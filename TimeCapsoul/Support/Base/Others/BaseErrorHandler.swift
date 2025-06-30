//
//  BaseErrorHandler.swift
//  TimeCapsoul
//
//  Created by Mehmet  Demir on 30.06.2025.
//

import Foundation
import UIKit

public protocol BaseErrorHandler {
    func handle(_ error: Error, on view: BaseView?)
}

public final class DefaultErrorHandler: BaseErrorHandler {
    public init() {}

    public func handle(_ error: Error, on view: BaseView?) {
        view?.showError(error.localizedDescription)
        // İster alert göster, ister logla, ister toast yap.
    }
}
