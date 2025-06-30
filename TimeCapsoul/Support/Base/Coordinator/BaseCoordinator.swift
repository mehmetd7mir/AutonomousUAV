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
    weak var parentCoordinator: Coordinator?
    var childCoordinators: [Coordinator] = []
    
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
        childCoordinators = childCoordinators.filter{$0 !== coordinator}
    }
    
    // MARK: - Debug
    deinit {
        print("\(String(describing: self)) deallocated")
    }
}
