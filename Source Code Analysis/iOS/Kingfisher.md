# [Kingfisher(7.7.0)](https://github.com/onevcat/Kingfisher/tree/7.7.0)

## 基本用法
```swift
import Kingfisher

let url = URL(string: "https://example.com/image.png")
imageView.kf.setImage(with: url)
```

## `KingfisherCompatible` & `KingfisherCompatibleValue`

查看 `kf` 属性，在 `KingfisherCompatible` 和 `KingfisherCompatibleValue` 中，位于 [`Kingfisher.swift`](https://github.com/onevcat/Kingfisher/blob/7.7.0/Sources/General/Kingfisher.swift)。

`kf` 类型为 `KingfisherWrapper` 结构体。

```swift
public struct KingfisherWrapper<Base> {
    public let base: Base
    public init(_ base: Base) {
        self.base = base
    }
}

public protocol KingfisherCompatible: AnyObject { }

public protocol KingfisherCompatibleValue {}

extension KingfisherCompatible {
    public var kf: KingfisherWrapper<Self> {
        get { return KingfisherWrapper(self) }
        set { }
    }
}

extension KingfisherCompatibleValue {
    public var kf: KingfisherWrapper<Self> {
        get { return KingfisherWrapper(self) }
        set { }
    }
}
```

## `KingfisherWrapper`

查看 `setImage(with resource: Resource?, placeholder: Placeholder? = nil, options: KingfisherOptionsInfo? = nil, completionHandler: ((Result<RetrieveImageResult, KingfisherError>) -> Void)? = nil) -> DownloadTask?` 方法，位于 [`ImageView+Kingfisher.swift`](https://github.com/onevcat/Kingfisher/blob/7.7.0/Sources/Extensions/ImageView%2BKingfisher.swift)。

```swift
extension KingfisherWrapper where Base: KFCrossPlatformImageView {
    @discardableResult
    public func setImage(
        with resource: Resource?,
        placeholder: Placeholder? = nil,
        options: KingfisherOptionsInfo? = nil,
        completionHandler: ((Result<RetrieveImageResult, KingfisherError>) -> Void)? = nil) -> DownloadTask?
    {
        return setImage(
            with: resource,
            placeholder: placeholder,
            options: options,
            progressBlock: nil,
            completionHandler: completionHandler
        )
    }
}
```

最终为调用 `setImage(with source: Source?, placeholder: Placeholder? = nil, parsedOptions: KingfisherParsedOptionsInfo, progressBlock: DownloadProgressBlock? = nil, completionHandler: ((Result<RetrieveImageResult, KingfisherError>) -> Void)? = nil) -> DownloadTask?` 方法。

```swift
func setImage(
    with source: Source?,
    placeholder: Placeholder? = nil,
    parsedOptions: KingfisherParsedOptionsInfo,
    progressBlock: DownloadProgressBlock? = nil,
    completionHandler: ((Result<RetrieveImageResult, KingfisherError>) -> Void)? = nil) -> DownloadTask?
{
    var mutatingSelf = self
    guard let source = source else {
        mutatingSelf.placeholder = placeholder
        mutatingSelf.taskIdentifier = nil
        completionHandler?(.failure(KingfisherError.imageSettingError(reason: .emptySource)))
        return nil
    }

    var options = parsedOptions

    let isEmptyImage = base.image == nil && self.placeholder == nil
    if !options.keepCurrentImageWhileLoading || isEmptyImage {
        // Always set placeholder while there is no image/placeholder yet.
        mutatingSelf.placeholder = placeholder
    }

    let maybeIndicator = indicator
    maybeIndicator?.startAnimatingView()

    let issuedIdentifier = Source.Identifier.next()
    mutatingSelf.taskIdentifier = issuedIdentifier

    if base.shouldPreloadAllAnimation() {
        options.preloadAllAnimationData = true
    }

    if let block = progressBlock {
        options.onDataReceived = (options.onDataReceived ?? []) + [ImageLoadingProgressSideEffect(block)]
    }

    let task = KingfisherManager.shared.retrieveImage(
        with: source,
        options: options,
        downloadTaskUpdated: { mutatingSelf.imageTask = $0 },
        progressiveImageSetter: { self.base.image = $0 },
        referenceTaskIdentifierChecker: { issuedIdentifier == self.taskIdentifier },
        completionHandler: { result in
            CallbackQueue.mainCurrentOrAsync.execute {
                maybeIndicator?.stopAnimatingView()
                guard issuedIdentifier == self.taskIdentifier else {
                    let reason: KingfisherError.ImageSettingErrorReason
                    do {
                        let value = try result.get()
                        reason = .notCurrentSourceTask(result: value, error: nil, source: source)
                    } catch {
                        reason = .notCurrentSourceTask(result: nil, error: error, source: source)
                    }
                    let error = KingfisherError.imageSettingError(reason: reason)
                    completionHandler?(.failure(error))
                    return
                }

                mutatingSelf.imageTask = nil
                mutatingSelf.taskIdentifier = nil

                switch result {
                case .success(let value):
                    guard self.needsTransition(options: options, cacheType: value.cacheType) else {
                        mutatingSelf.placeholder = nil
                        self.base.image = value.image
                        completionHandler?(result)
                        return
                    }

                    self.makeTransition(image: value.image, transition: options.transition) {
                        completionHandler?(result)
                    }

                case .failure:
                    if let image = options.onFailureImage {
                        mutatingSelf.placeholder = nil
                        self.base.image = image
                    }
                    completionHandler?(result)
                }
            }
        }
    )
    mutatingSelf.imageTask = task
    return task
}
```

## 总结

* 使用 `ConstraintViewDSL` 进行命名空间的统一收拢。
* `ConstraintRelatableTarget` 使用协议来整合基础类型，方便作为参数使用。
* `ConstraintMakerExtendable` 使用继承分模块拓展属性。
* `ConstraintAttributes` 使用 `OptionSet` 来增加可读性。
* `left`、`top`、`bottom`、`right` 返回自身类型 `ConstraintMakerExtendable`，实现链式调用。
