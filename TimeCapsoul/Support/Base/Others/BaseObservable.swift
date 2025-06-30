//
//  BaseObservable.swift
//  TimeCapsoul
//
//  Created by Mehmet  Demir on 30.06.2025.
//

import RxSwift
import Foundation

public protocol BaseObservable: AnyObject {
    var disposeBag: DisposeBag { get }
}

public extension BaseObservable {
    var disposeBag: DisposeBag {
        let key = UnsafeRawPointer(bitPattern: "disposeBag".hashValue)!
        if let bag = objc_getAssociatedObject(self, key) as? DisposeBag {
            return bag
        } else {
            let bag = DisposeBag()
            objc_setAssociatedObject(self, key, bag, .OBJC_ASSOCIATION_RETAIN_NONATOMIC)
            return bag
        }
    }
}
