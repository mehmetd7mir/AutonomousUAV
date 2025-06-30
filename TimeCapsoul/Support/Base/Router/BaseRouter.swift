//
//  BaseRouter.swift
//  TimeCapsoul
//
//  Created by Mehmet  Demir on 23.06.2025.
//

import UIKit

protocol BaseRouter: AnyObject {
    var navigationController: UINavigationController? { get set }

    init(navigationController: UINavigationController?)

    func push(_ viewController: UIViewController, animated: Bool)
    func present(_ viewController: UIViewController, animated: Bool)
    func pop(animated: Bool)
    func dismiss(animated: Bool)
}

extension BaseRouter {
    func push(_ viewController: UIViewController, animated: Bool = true) {
        navigationController?.pushViewController(viewController, animated: animated)
    }

    func pop(animated: Bool = true) {
        navigationController?.popViewController(animated: animated)
    }

    func present(_ viewController: UIViewController, animated: Bool = true, completion: (() -> Void)? = nil) {
        navigationController?.present(viewController, animated: animated, completion: completion)
    }

    func dismiss(animated: Bool = true, completion: (() -> Void)? = nil) {
        navigationController?.dismiss(animated: animated, completion: completion)
    }
}
