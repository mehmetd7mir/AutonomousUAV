//
//  BaseCoordinator.swift
//  TimeCapsoul
//
//  Created by Mehmet  Demir on 23.06.2025.
//

import UIKit

class BaseCoordinator : Coordinator {
    
    // MARK: - Properties
    var navigationController: UINavigationController
    weak var parentCoordinator: Coordinator? // must be weak avoid the memory leak/retain cycle
    private( set )  var childCoordinators: [Coordinator] = []
    
    // MARK: - Init
    init(navigationController: UINavigationController) {
        self.navigationController = navigationController
    }
    
    // MARK: - Abstract Start
    func start() {
        fatalError("Must be implemented by subclass")
    }
    
    // MARK: - Child Management
    func add(_ coordinator: any Coordinator) {
        coordinator.parentCoordinator = self
        childCoordinators.append(coordinator)
        
    }
    
    func remove(_ coordinator: any Coordinator) {
        if let index = childCoordinators.firstIndex(where: { $0 === coordinator }) {
                childCoordinators.remove(at: index)
            }
    }
    
    // MARK: - Debug
    deinit {
        print("\(String(describing: self)) deallocated")
        parentCoordinator?.remove(self) // this is essential for memory leak
    }
}


/* Learning

 any Coordinator means using the protocol itself as a type.
 It allows holding different Coordinator conforming classes (e.g., OnboardingCoordinator, HomeCoordinator).
 Swift requires "any" keyword to "explicitly indicate" existential types since Swift 5.7+.
 Without "any" Swift cannot infer the exact type and throws a compile-time error.
 "any" means "any instance that conforms to Coordinator, regardless of its concrete type".
        
 String(describing : self) is name of class without describing : self is memory adress
 String(describing : self) likely self.name
 describing belogs to String
 
 uing firstIndex + remove(at:) instead of filter
 Mmore efficient because it stops at first match
 filter checks all items and creates new array (less efficient)
 
*/
