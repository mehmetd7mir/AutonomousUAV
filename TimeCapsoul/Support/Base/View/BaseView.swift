//
//  BaseView.swift
//  TimeCapsoul
//
//  Created by Mehmet Demir on 23.06.2025.
//

import UIKit
import Foundation

public protocol BaseView: AnyObject {
    func showLoading(_ isLoading: Bool)
    func showError(_ error: String)
}

