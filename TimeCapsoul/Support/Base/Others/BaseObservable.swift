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

/* Learning
 
        *   Reactive Programing with RxS.  *
    Observer : Listening the event , to react
    Observable : publish event/data
    observer should subscript the observable notfications
    DisposeBag : break the connection of observer-observable , it is essential for memory leak
 
        * Reason | Why do we use Extension here | Critical Point *

    swift protocol doesn't support stored property directly
    by using extension with objc_getAssociatedObject, we can dynamically add disposeBag to any class that conforms to BaseObservable
    this avoids writing 'var disposeBag = DisposeBag()' in every class manually. // dry - dont repeat yourself
   
    
        * Objective C  ---bridge---  Swift   *
    In objective c, we can add new property to object after runtime or in runtime.But there isnt in swift.
    UnsafeRawPointer : It is like a key. Unique key for memory address.It doesnt hold any value, only point to memory.
    bjc_getAssociatedObject : Check if object already has disposeBag in memory.If it has, return it.
    objc_setAssociatedObject : If doesnt have, create new disposeBag and set to object in memory.
    .OBJC_ASSOCIATION_RETAIN_NONATOMIC : This means keep object in memory strong.
    Nonatomic : It is not thread safe, but faster.
    All in all : This code adds disposeBag to any class which conforms BaseObservable protocol.
     
*/
