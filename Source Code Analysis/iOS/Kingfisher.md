# [Kingfisher(7.7.0)](https://github.com/onevcat/Kingfisher/tree/7.7.0)

## 基本用法
```swift
import Kingfisher

let url = URL(string: "https://example.com/image.png")
imageView.kf.setImage(with: url)
```

## 总结

* 使用 `ConstraintViewDSL` 进行命名空间的统一收拢。
* `ConstraintRelatableTarget` 使用协议来整合基础类型，方便作为参数使用。
* `ConstraintMakerExtendable` 使用继承分模块拓展属性。
* `ConstraintAttributes` 使用 `OptionSet` 来增加可读性。
* `left`、`top`、`bottom`、`right` 返回自身类型 `ConstraintMakerExtendable`，实现链式调用。
