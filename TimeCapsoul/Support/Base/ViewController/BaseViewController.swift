//
//  BaseViewController.swift
//  TimeCapsoul
//
//  Created by Mehmet Demir on 23.06.2025.
//

import UIKit

class BaseViewController: UIViewController, BaseView {

    // MARK: - Lifecycle
    override func viewDidLoad() {
        super.viewDidLoad()
        setupUI()
        setupLocalization()
        setupAccessibility()
        setupBindings()
    }

    // MARK: - UI Setup Hooks
    func setupUI() {}
    func setupAccessibility() {}
    func setupBindings() {}
    func setupLocalization() {
        localize()
    }
    @objc func localize(){}
    // MARK: - BaseView Protocol
    func showLoading(_ isLoading: Bool) {
        // Default no-op
    }

    func showError(_ message: String) {
        // Default no-op
    }
}
