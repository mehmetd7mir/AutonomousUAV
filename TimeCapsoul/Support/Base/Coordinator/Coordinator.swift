//
//  CoordinatorProtocol.swift
//  TimeCapsoul
//
//  Created by Mehmet  Demir on 30.06.2025.
//

import Foundation
import UIKit

protocol Coordinator : AnyObject {
    
    var navigationController : UINavigationController { get }
    
    /** weak * */  var parentCoordinator : Coordinator? { get set } // must be weak by implemented class
    
    var childCoordinators: [Coordinator] { get }
    
    func start() // Every coordinator start own flow,which screen to show first and how the flow begins.
    
    func add(_ coordinator : Coordinator)
    
    func remove(_ coordinator : Coordinator)
    
}

/* Learning  
    
    Value Type : struct, enum  ( i can say pass by value )
    Reference type : class , actor ( All operations are performed on/with the original object )
    
    
    *** What is WEAK/STRONG REFERENCE ? ***
    init() = bismillah / the beginnig of life
    deinit() = can bedenden cıkma / the end of life
    Strong R. : This is hold/keep the two objects each other and as long as one of them holds the other , the object CANNOT be deallocated.
    Weak R. : İf one of them will be nil the other continue own way, no problem
    - Use strong if ownership is required.
    - Use weak if it's just a reference, not ownership.
    
    obj.deinit() -- totaly stupidity
    
    
*/
