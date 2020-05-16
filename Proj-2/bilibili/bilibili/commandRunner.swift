//
//  commandRunner.swift
//  bilibili_1
//
//  Created by HUi on 20200308.
//  Copyright © 2020 HUi. All rights reserved.
//

import Foundation

// MARK: ErroRs
/// This is a customized error enum. It has type of (.allGood), (.notFound), (.httpError)
enum ERRoR: Error {
    case allGood
    case notFound(String)
    case httpError(Int, String)
}

// MARK: runCommand
/// This function will return the command's output,  the  state code and throw  an  ERRoR state
func runCommand(_ bin: String, isPrint: Bool = false, arguments: [String], runtime: Int = 1) throws -> (String, Int) {
    let pipe = Pipe()
    let file = pipe.fileHandleForReading
    var launchPath = bin

    if launchPath.first != "/" || launchPath != "/usr/bin/which" {
        launchPath = try! runCommand("/usr/bin/which", arguments: [launchPath], runtime: 2).0
    }

    if launchPath.isEmpty || launchPath.first != "/" {
        throw ERRoR.notFound("command not found")
    } else {
        if launchPath.last == "\n" {
            launchPath = String(launchPath.dropLast())
        }
        let task = Process()
        task.launchPath = launchPath
        task.arguments = arguments
        task.standardOutput = pipe
        try! task.run()
        task.waitUntilExit()

        let data = file.readDataToEndOfFile()
        if runtime == 1, isPrint {
            print(String(data: data, encoding: String.Encoding.utf8)!)
        }
        var returnString = String(data: data, encoding: String.Encoding.utf8)!
        if returnString.last == "\n" {
            returnString = String(returnString.dropLast())
        }
        return (returnString, Int(task.terminationStatus))
    }
}
