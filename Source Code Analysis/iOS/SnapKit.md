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

## `ConstraintView`
查看 `snp` 属性，有 3 处，位于 [`ConstraintView+Extensions.swift`](https://github.com/SnapKit/SnapKit/blob/5.6.0/Sources/ConstraintView%2BExtensions.swift)、[`UILayoutSupport+Extensions.swift`](https://github.com/SnapKit/SnapKit/blob/5.6.0/Sources/UILayoutSupport%2BExtensions.swift)、[`ConstraintLayoutGuide+Extensions.swift`](https://github.com/SnapKit/SnapKit/blob/5.6.0/Sources/ConstraintLayoutGuide%2BExtensions.swift)。
```swift
public extension ConstraintView {
    var snp: ConstraintViewDSL {
        return ConstraintViewDSL(view: self)
    }
}
```

```swift
@available(iOS 8.0, *)
public extension ConstraintLayoutSupport {
    var snp: ConstraintLayoutSupportDSL {
        return ConstraintLayoutSupportDSL(support: self)
    }
}
```

```swift
@available(iOS 9.0, OSX 10.11, *)
public extension ConstraintLayoutGuide {
    var snp: ConstraintLayoutGuideDSL {
        return ConstraintLayoutGuideDSL(guide: self)
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

## `ConstraintViewDSL`
查看 `ConstraintViewDSL` 类，为遵循 `ConstraintAttributesDSL` 协议的结构体，位于 [`ConstraintViewDSL.swift`](https://github.com/SnapKit/SnapKit/blob/5.6.0/Sources/ConstraintViewDSL.swift)。
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


