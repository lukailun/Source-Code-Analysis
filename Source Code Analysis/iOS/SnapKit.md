# [SnapKit(5.6.0)](https://github.com/SnapKit/SnapKit/tree/5.6.0)

## 基本用法
```swift
import SnapKit

class MyViewController: UIViewController {

    lazy var box = UIView()
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        view.addSubview(box)
        box.backgroundColor = .green
        box.snp.makeConstraints { make in
           make.width.height.equalTo(50)
           make.center.equalTo(view)
        }
    }
}
```

## `ConstraintView` & `ConstraintLayoutSupport` & `ConstraintLayoutGuide`
SnapKit 对 View、LayoutSupport、LayoutGuide 进行了统一的封装。

查看 `snp` 属性，有 3 处，位于 [`ConstraintView+Extensions.swift`](https://github.com/SnapKit/SnapKit/blob/5.6.0/Sources/ConstraintView%2BExtensions.swift)、[`UILayoutSupport+Extensions.swift`](https://github.com/SnapKit/SnapKit/blob/5.6.0/Sources/UILayoutSupport%2BExtensions.swift)、[`ConstraintLayoutGuide+Extensions.swift`](https://github.com/SnapKit/SnapKit/blob/5.6.0/Sources/ConstraintLayoutGuide%2BExtensions.swift)。

```swift
public extension ConstraintView {
    var snp: ConstraintViewDSL {
        return ConstraintViewDSL(view: self)
    }
}
```

查看 `ConstraintView` 类，为 `UIView`/`NSView` 的类型别名，位于 [`ConstraintView.swift`](https://github.com/SnapKit/SnapKit/blob/5.6.0/Sources/ConstraintView.swift)。

```swift
#if os(iOS) || os(tvOS)
    public typealias ConstraintView = UIView
#else
    public typealias ConstraintView = NSView
#endif
```

---

```swift
@available(iOS 8.0, *)
public extension ConstraintLayoutSupport {
    var snp: ConstraintLayoutSupportDSL {
        return ConstraintLayoutSupportDSL(support: self)
    }
}
```

查看 `ConstraintLayoutSupport` 类，为 `UILayoutSupport` 的类型别名，位于 [`ConstraintLayoutSupport.swift`](https://github.com/SnapKit/SnapKit/blob/5.6.0/Sources/ConstraintLayoutSupport.swift)。

```swift
#if os(iOS) || os(tvOS)
    @available(iOS 8.0, *)
    public typealias ConstraintLayoutSupport = UILayoutSupport
#else
    public class ConstraintLayoutSupport {}
#endif
```

---

```swift
@available(iOS 9.0, OSX 10.11, *)
public extension ConstraintLayoutGuide {
    var snp: ConstraintLayoutGuideDSL {
        return ConstraintLayoutGuideDSL(guide: self)
    }
}
```

查看 `ConstraintLayoutGuide` 类，为 `UILayoutGuide`/`NSLayoutGuide` 的类型别名，位于 [`ConstraintLayoutGuide.swift`](https://github.com/SnapKit/SnapKit/blob/5.6.0/Sources/ConstraintLayoutGuide.swift)。

```swift
#if os(iOS) || os(tvOS)
    @available(iOS 9.0, *)
    public typealias ConstraintLayoutGuide = UILayoutGuide
#else
    @available(OSX 10.11, *)
    public typealias ConstraintLayoutGuide = NSLayoutGuide
#endif
```

## `ConstraintViewDSL`
查看 `ConstraintViewDSL` 类，为遵循 `ConstraintAttributesDSL` 协议的结构体，位于 [`ConstraintViewDSL.swift`](https://github.com/SnapKit/SnapKit/blob/5.6.0/Sources/ConstraintViewDSL.swift)。

其中，持有属性 `view`。因为 `ConstraintViewDSL` 为 `struct`，没有引用计数，所以不会造成循环引用。

```swift
public struct ConstraintViewDSL: ConstraintAttributesDSL {
    public var target: AnyObject? {
        return self.view
    }
    
    internal let view: ConstraintView
    
    internal init(view: ConstraintView) {
        self.view = view   
    }
}
```

查看 `ConstraintAttributesDSL` 协议、`ConstraintBasicAttributesDSL` 协议、`ConstraintDSL` 协议，位于 [`ConstraintDSL.swift`](https://github.com/SnapKit/SnapKit/blob/5.6.0/Sources/ConstraintDSL.swift)。

```swift
public protocol ConstraintAttributesDSL: ConstraintBasicAttributesDSL {}

public protocol ConstraintBasicAttributesDSL: ConstraintDSL {}

public protocol ConstraintDSL {
    var target: AnyObject? { get }
    
    func setLabel(_ value: String?)
    func label() -> String?
}
```

查看 `ConstraintViewDSL` 中最常用的设置约束的几个方法。

```swift
@discardableResult
public func prepareConstraints(_ closure: (_ make: ConstraintMaker) -> Void) -> [Constraint] {
    return ConstraintMaker.prepareConstraints(item: self.view, closure: closure)
}

public func makeConstraints(_ closure: (_ make: ConstraintMaker) -> Void) {
    ConstraintMaker.makeConstraints(item: self.view, closure: closure)
}

public func remakeConstraints(_ closure: (_ make: ConstraintMaker) -> Void) {
    ConstraintMaker.remakeConstraints(item: self.view, closure: closure)
}

public func updateConstraints(_ closure: (_ make: ConstraintMaker) -> Void) {
    ConstraintMaker.updateConstraints(item: self.view, closure: closure)
}

public func removeConstraints() {
    ConstraintMaker.removeConstraints(item: self.view)
}
```

## `ConstraintMaker`
查看 `ConstraintMaker` 类，位于 [`ConstraintMaker.swift`](https://github.com/SnapKit/SnapKit/blob/5.6.0/Sources/ConstraintMaker.swift)。

```swift
public class ConstraintMaker {
    internal static func prepareConstraints(item: LayoutConstraintItem, closure: (_ make: ConstraintMaker) -> Void) -> [Constraint] {
        let maker = ConstraintMaker(item: item)
        closure(maker)
        var constraints: [Constraint] = []
        for description in maker.descriptions {
            guard let constraint = description.constraint else {
                continue
            }
            constraints.append(constraint)
        }
        return constraints
    }

    internal static func makeConstraints(item: LayoutConstraintItem, closure: (_ make: ConstraintMaker) -> Void) {
        let constraints = prepareConstraints(item: item, closure: closure)
        for constraint in constraints {
            constraint.activateIfNeeded(updatingExisting: false)
        }
    }

    internal static func remakeConstraints(item: LayoutConstraintItem, closure: (_ make: ConstraintMaker) -> Void) {
        self.removeConstraints(item: item)
        self.makeConstraints(item: item, closure: closure)
    }

    internal static func updateConstraints(item: LayoutConstraintItem, closure: (_ make: ConstraintMaker) -> Void) {
        guard item.constraints.count > 0 else {
            self.makeConstraints(item: item, closure: closure)
            return
        }

        let constraints = prepareConstraints(item: item, closure: closure)
        for constraint in constraints {
            constraint.activateIfNeeded(updatingExisting: true)
        }
    }

    internal static func removeConstraints(item: LayoutConstraintItem) {
        let constraints = item.constraints
        for constraint in constraints {
            constraint.deactivateIfNeeded()
        }
    }
}
```

统一调用了 `prepareConstraints(item: LayoutConstraintItem, closure: (_ make: ConstraintMaker) -> Void) -> [Constraint]` 方法，创建一个新的 `ConstraintMaker` 并通过 `closure` 将添加约束的代码进行调用。

`ConstraintMaker` 中定义了一系列常用的属性 `left`、`top`、`bottom`、`right` 等。

```swift
public var left: ConstraintMakerExtendable {
    return self.makeExtendableWithAttributes(.left)
}

public var top: ConstraintMakerExtendable {
    return self.makeExtendableWithAttributes(.top)
}

public var bottom: ConstraintMakerExtendable {
    return self.makeExtendableWithAttributes(.bottom)
}
    
public var right: ConstraintMakerExtendable {
    return self.makeExtendableWithAttributes(.right)
}
```


