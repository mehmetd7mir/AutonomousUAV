//
//  BaseViewController.swift
//  TimeCapsoul
//
//  Created by Mehmet Demir on 23.06.2025.
//

import UIKit
import RxSwift
import RxCocoa

class BaseViewController: UIViewController, BaseView {
    
    let disposeBag = DisposeBag()
    
    // MARK: - Lifecycle
    override func viewDidLoad() {
        super.viewDidLoad()
        setupUI()
        setupLocalization()
        setupBindings()
        setupAccessibility()
    }

    // MARK: - UI Setup Hooks
    func setupUI() {}
    func setupAccessibility() {}
    func setupBindings() {}
    
    func setupLocalization() {
        LanguageManager.shared.currentLanguage
            .distinctUntilChanged()
            .observe(on: MainScheduler.instance)
            .subscribe(onNext: {
                [weak self] _ in
                self?.localize()
                self?.setupAccessibility()
            })
            .disposed(by: disposeBag)
    }
    
    @objc func localize(){
        setupAccessibility() // ensure accessibility labels are updated too
        // we should override in every viewc. and set every translate of every element and hint
    }
    
    // MARK: - BaseView Protocol
    func showLoading(_ isLoading: Bool) {
        // Default no-op
    }

    func showError(_ message: String) {
        // Default no-op
    }
}

/*  Learning
           ***  RxSwift/Cocoa   ***
    Observable     :  data to listening
    Observer       :  it is who listening the data
    subscribe      :  starting the listen
    onNext         :  what happens when new data comes
    dispose        :  interrup to listen
    BehaviorRelay  :  always keeps the updated data
    
    RxSwift : change language, network , login state ...
    RxCocoa : listen the UIKit and its components(labels,buttons , picker etc.)
    
    .distincUntilChanged() : if coming thing is same do nothing if not then continue | Only running when diffent value comes
    .skip(n) : Skip the the first comes "n" element.
    
 */
