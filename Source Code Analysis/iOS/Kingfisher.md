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

```

## 总结

* 使用 `ConstraintViewDSL` 进行命名空间的统一收拢。
* `ConstraintRelatableTarget` 使用协议来整合基础类型，方便作为参数使用。
* `ConstraintMakerExtendable` 使用继承分模块拓展属性。
* `ConstraintAttributes` 使用 `OptionSet` 来增加可读性。
* `left`、`top`、`bottom`、`right` 返回自身类型 `ConstraintMakerExtendable`，实现链式调用。
