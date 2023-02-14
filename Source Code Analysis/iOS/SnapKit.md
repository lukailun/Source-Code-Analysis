# [SnapKit](https://github.com/SnapKit/SnapKit)

基本用法。
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

查看 `snp` 属性，位于 `ConstraintView+Extensions.swift`。
```swift
public extension ConstraintView {
    var snp: ConstraintViewDSL {
        return ConstraintViewDSL(view: self)
    }
}
```

`ConstraintView` 类，位于 `ConstraintView.swift`。
```swift
#if os(iOS) || os(tvOS)
    public typealias ConstraintView = UIView
#else
    public typealias ConstraintView = NSView
#endif
```
