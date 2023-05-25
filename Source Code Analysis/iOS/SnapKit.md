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

查看 `ConstraintView`，为 `UIView`/`NSView` 的类型别名，位于 [`ConstraintView.swift`](https://github.com/SnapKit/SnapKit/blob/5.6.0/Sources/ConstraintView.swift)。

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

查看 `ConstraintLayoutSupport`，为 `UILayoutSupport` 的类型别名，位于 [`ConstraintLayoutSupport.swift`](https://github.com/SnapKit/SnapKit/blob/5.6.0/Sources/ConstraintLayoutSupport.swift)。

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

查看 `ConstraintLayoutGuide`，为 `UILayoutGuide`/`NSLayoutGuide` 的类型别名，位于 [`ConstraintLayoutGuide.swift`](https://github.com/SnapKit/SnapKit/blob/5.6.0/Sources/ConstraintLayoutGuide.swift)。

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
查看 `ConstraintViewDSL`，为遵循 `ConstraintAttributesDSL` 协议的结构体，位于 [`ConstraintViewDSL.swift`](https://github.com/SnapKit/SnapKit/blob/5.6.0/Sources/ConstraintViewDSL.swift)。

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

查看 `ConstraintAttributesDSL`、`ConstraintBasicAttributesDSL`、`ConstraintDSL`，位于 [`ConstraintDSL.swift`](https://github.com/SnapKit/SnapKit/blob/5.6.0/Sources/ConstraintDSL.swift)。

```swift
public protocol ConstraintAttributesDSL: ConstraintBasicAttributesDSL {}

public protocol ConstraintBasicAttributesDSL: ConstraintDSL {}

public protocol ConstraintDSL {
    var target: AnyObject? { get }
    
    func setLabel(_ value: String?)
    func label() -> String?
}
```

查看 `ConstraintViewDSL` 中几个最常用的设置约束的方法。

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
查看 `ConstraintMaker`，位于 [`ConstraintMaker.swift`](https://github.com/SnapKit/SnapKit/blob/5.6.0/Sources/ConstraintMaker.swift)。

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

`ConstraintMaker` 中定义了一系列常用的属性 `left`、`top`、`bottom`、`right` 等，都为 `ConstraintMakerExtendable` 类型。

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

## `ConstraintMakerExtendable` & `ConstraintMakerRelatable`
查看 `ConstraintMakerExtendable`，为继承 `ConstraintMakerRelatable` 的类，位于 [`ConstraintMakerExtendable.swift`](https://github.com/SnapKit/SnapKit/blob/5.6.0/Sources/ConstraintMakerExtendable.swift)。

```swift
public class ConstraintMakerExtendable: ConstraintMakerRelatable {
    
    public var left: ConstraintMakerExtendable {
        self.description.attributes += .left
        return self
    }
    
    public var top: ConstraintMakerExtendable {
        self.description.attributes += .top
        return self
    }
    
    public var bottom: ConstraintMakerExtendable {
        self.description.attributes += .bottom
        return self
    }
    
    public var right: ConstraintMakerExtendable {
        self.description.attributes += .right
        return self
    }
}
```

查看 `ConstraintMakerRelatable`，位于 [`ConstraintMakerExtendable.swift`](https://github.com/SnapKit/SnapKit/blob/5.6.0/Sources/ConstraintMakerRelatable.swift)。

```swift
public class ConstraintMakerRelatable {

    internal let description: ConstraintDescription
    
    internal init(_ description: ConstraintDescription) {
        self.description = description
    }
    
    internal func relatedTo(_ other: ConstraintRelatableTarget, relation: ConstraintRelation, file: String, line: UInt) -> ConstraintMakerEditable {
        let related: ConstraintItem
        let constant: ConstraintConstantTarget
        
        if let other = other as? ConstraintItem {
            guard other.attributes == ConstraintAttributes.none ||
                  other.attributes.layoutAttributes.count <= 1 ||
                  other.attributes.layoutAttributes == self.description.attributes.layoutAttributes ||
                  other.attributes == .edges && self.description.attributes == .margins ||
                  other.attributes == .margins && self.description.attributes == .edges ||
                  other.attributes == .directionalEdges && self.description.attributes == .directionalMargins ||
                  other.attributes == .directionalMargins && self.description.attributes == .directionalEdges else {
                fatalError("Cannot constraint to multiple non identical attributes. (\(file), \(line))");
            }
            
            related = other
            constant = 0.0
        } else if let other = other as? ConstraintView {
            related = ConstraintItem(target: other, attributes: ConstraintAttributes.none)
            constant = 0.0
        } else if let other = other as? ConstraintConstantTarget {
            related = ConstraintItem(target: nil, attributes: ConstraintAttributes.none)
            constant = other
        } else if #available(iOS 9.0, OSX 10.11, *), let other = other as? ConstraintLayoutGuide {
            related = ConstraintItem(target: other, attributes: ConstraintAttributes.none)
            constant = 0.0
        } else {
            fatalError("Invalid constraint. (\(file), \(line))")
        }
        
        let editable = ConstraintMakerEditable(self.description)
        editable.description.sourceLocation = (file, line)
        editable.description.relation = relation
        editable.description.related = related
        editable.description.constant = constant
        return editable
    }
    
    @discardableResult
    public func equalTo(_ other: ConstraintRelatableTarget, _ file: String = #file, _ line: UInt = #line) -> ConstraintMakerEditable {
        return self.relatedTo(other, relation: .equal, file: file, line: line)
    }
    
    @discardableResult
    public func equalToSuperview(_ file: String = #file, _ line: UInt = #line) -> ConstraintMakerEditable {
        guard let other = self.description.item.superview else {
            fatalError("Expected superview but found nil when attempting make constraint `equalToSuperview`.")
        }
        return self.relatedTo(other, relation: .equal, file: file, line: line)
    }
}
```

统一调用了 `relatedTo(_ other: ConstraintRelatableTarget, relation: ConstraintRelation, file: String, line: UInt) -> ConstraintMakerEditable` 方法，约束相关的所有信息都在 `description` 中。

## `ConstraintDescription`
查看 `ConstraintDescription`，位于 [`ConstraintDescription.swift`](https://github.com/SnapKit/SnapKit/blob/5.6.0/Sources/ConstraintDescription.swift)。

```swift
public class ConstraintDescription {
    
    internal let item: LayoutConstraintItem
    internal var attributes: ConstraintAttributes
    internal var relation: ConstraintRelation? = nil
    internal var sourceLocation: (String, UInt)? = nil
    internal var label: String? = nil
    internal var related: ConstraintItem? = nil
    internal var multiplier: ConstraintMultiplierTarget = 1.0
    internal var constant: ConstraintConstantTarget = 0.0
    internal var priority: ConstraintPriorityTarget = 1000.0
    internal lazy var constraint: Constraint? = {
        guard let relation = self.relation,
              let related = self.related,
              let sourceLocation = self.sourceLocation else {
            return nil
        }
        let from = ConstraintItem(target: self.item, attributes: self.attributes)
        
        return Constraint(
            from: from,
            to: related,
            relation: relation,
            sourceLocation: sourceLocation,
            label: self.label,
            multiplier: self.multiplier,
            constant: self.constant,
            priority: self.priority
        )
    }()
    
    // MARK: Initialization
    
    internal init(item: LayoutConstraintItem, attributes: ConstraintAttributes) {
        self.item = item
        self.attributes = attributes
    }
    
}
```

## `ConstraintAttributes`
查看 `ConstraintAttributes`，位于 [`ConstraintAttributes.swift`](https://github.com/SnapKit/SnapKit/blob/5.6.0/Sources/ConstraintAttributes.swift)。

其中，使用 `OptionSet` 来使 left + top + right + bottom == edges，更优雅，可读性更高。

```swift
internal struct ConstraintAttributes : OptionSet, ExpressibleByIntegerLiteral {
    // normal
    internal static let none: ConstraintAttributes = 0
    internal static let left: ConstraintAttributes = ConstraintAttributes(UInt(1) << 0)
    internal static let top: ConstraintAttributes = ConstraintAttributes(UInt(1) << 1)
    internal static let right: ConstraintAttributes = ConstraintAttributes(UInt(1) << 2)
    internal static let bottom: ConstraintAttributes = ConstraintAttributes(UInt(1) << 3)
    internal static let leading: ConstraintAttributes = ConstraintAttributes(UInt(1) << 4)
    internal static let trailing: ConstraintAttributes = ConstraintAttributes(UInt(1) << 5)
    internal static let width: ConstraintAttributes = ConstraintAttributes(UInt(1) << 6)
    internal static let height: ConstraintAttributes = ConstraintAttributes(UInt(1) << 7)
    internal static let centerX: ConstraintAttributes = ConstraintAttributes(UInt(1) << 8)
    internal static let centerY: ConstraintAttributes = ConstraintAttributes(UInt(1) << 9)
    internal static let lastBaseline: ConstraintAttributes = ConstraintAttributes(UInt(1) << 10)
    
    // aggregates
    
    internal static let edges: ConstraintAttributes = [.horizontalEdges, .verticalEdges]
    internal static let horizontalEdges: ConstraintAttributes = [.left, .right]
    internal static let verticalEdges: ConstraintAttributes = [.top, .bottom]
    internal static let directionalEdges: ConstraintAttributes = [.directionalHorizontalEdges, .directionalVerticalEdges]
    internal static let directionalHorizontalEdges: ConstraintAttributes = [.leading, .trailing]
    internal static let directionalVerticalEdges: ConstraintAttributes = [.top, .bottom]
    internal static let size: ConstraintAttributes = [.width, .height]
    internal static let center: ConstraintAttributes = [.centerX, .centerY]
}
```

## `Constraint`
查看 `Constraint`，位于 [`Constraint.swift`](https://github.com/SnapKit/SnapKit/blob/5.6.0/Sources/Constraint.swift)。

```swift
public final class Constraint {
    internal func activateIfNeeded(updatingExisting: Bool = false) {
        guard let item = self.from.layoutConstraintItem else {
            print("WARNING: SnapKit failed to get from item from constraint. Activate will be a no-op.")
            return
        }
        let layoutConstraints = self.layoutConstraints

        if updatingExisting {
            var existingLayoutConstraints: [LayoutConstraint] = []
            for constraint in item.constraints {
                existingLayoutConstraints += constraint.layoutConstraints
            }

            for layoutConstraint in layoutConstraints {
                let existingLayoutConstraint = existingLayoutConstraints.first { $0 == layoutConstraint }
                guard let updateLayoutConstraint = existingLayoutConstraint else {
                    fatalError("Updated constraint could not find existing matching constraint to update: \(layoutConstraint)")
                }

                let updateLayoutAttribute = (updateLayoutConstraint.secondAttribute == .notAnAttribute) ? updateLayoutConstraint.firstAttribute : updateLayoutConstraint.secondAttribute
                updateLayoutConstraint.constant = self.constant.constraintConstantTargetValueFor(layoutAttribute: updateLayoutAttribute)
            }
        } else {
            NSLayoutConstraint.activate(layoutConstraints)
            item.add(constraints: [self])
        }
    }

    internal func deactivateIfNeeded() {
        guard let item = self.from.layoutConstraintItem else {
            print("WARNING: SnapKit failed to get from item from constraint. Deactivate will be a no-op.")
            return
        }
        let layoutConstraints = self.layoutConstraints
        NSLayoutConstraint.deactivate(layoutConstraints)
        item.remove(constraints: [self])
    }
}
```

`activateIfNeeded(updatingExisting: Bool = false)` 和 `deactivateIfNeeded()` 方法分别将添加的约束生效和不生效。

>
