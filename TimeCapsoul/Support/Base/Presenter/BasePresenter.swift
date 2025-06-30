//
//  BasePresenter.swift
//  TimeCapsoul
//
//  Created by Mehmet  Demir on 23.06.2025.
//

import Foundation

public protocol BasePresenter: AnyObject {
    associatedtype View: BaseView

    var view: View? { get set }

    init(view: View)

    func viewDidLoad()
    func viewWillAppear()
    func viewDidAppear()
    func viewWillDisappear()
    func viewDidDisappear()
}
