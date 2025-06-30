//
//  CoordinatorProtocol.swift
//  TimeCapsoul
//
//  Created by Mehmet  Demir on 30.06.2025.
//

import Foundation
import UIKit

public protocol Coordinator : AnyObject {
    
    var navigationController : UINavigationController { get }
    
    var parentCoordinator : Coordinator? {get set}
    
    var childCoordinators : [Coordinator] {get set}
    
    func start()
    
    func add(_ coordinator : Coordinator)
    
    func remove(_ coordinator : Coordinator)
    
}

/* Learning
    We use AnyObject for using this protocol in own. so reference type
    
 
*/
