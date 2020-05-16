//
//  main.swift
//  bilibili_1
//
//  Created by HUi on 20200308.
//  Copyright © 2020 HUi. All rights reserved.
//

import Foundation

print("Hello, World!")

// Basic Settings
let FManager = FileManager.default

//目录 #1: /Users/HUi/usrtmp/bilibili/content/
let rootPath = "/Users/HUi/usrtmp/bilibili/content/"
let rootURL = URL(fileURLWithPath: rootPath)
let pianPathSet = try! FManager.contentsOfDirectory(atPath: rootURL.path)
// 第一次循环,/Users/HUi/usrtmp/bilibili/content/, 获取“篇”
for pianSubPath in pianPathSet {
    if pianSubPath != ".DS_Store" { //排除 #系统文件
        //目录 #2: /Users/HUi/usrtmp/bilibili/content/
        let pianPath = rootPath + pianSubPath
        let pianURL = URL(fileURLWithPath: pianPath)
        let volPathSet = try! FManager.contentsOfDirectory(atPath: pianURL.path)
        // 第二次循环，/Users/HUi/usrtmp/bilibili/content/篇*, 获取“话”
        for volSubPath in volPathSet {
            if volSubPath != ".DS_Store" {
                let volPath = pianPath + "/" + volSubPath
                let volURL = URL(fileURLWithPath: volPath)
                let chapterPathSet = try! FManager.contentsOfDirectory(atPath: volURL.path)
                // 第三次循环, /Users/HUi/usrtmp/bilibili/content/篇*/话*, 获取"页"
                for chapterSubPath in chapterPathSet {
                    if chapterSubPath != ".DS_Store" {
                        let chapterPath = volPath + "/" + chapterSubPath
                        let chapterURL = URL(fileURLWithPath: chapterPath)
                        var chapterNameS: String = ""
                        var chapterNameT: String = ""
                        var isRecordHua: Bool = false
                        //记录“话”
                        for i in chapterSubPath {
                            if i == "第", !isRecordHua {
                                isRecordHua = true
                            }
                            if isRecordHua {
                                chapterNameS += String(i)
                                //转化为简体
                                if i == "话" {
                                    chapterNameT += "話"
                                } else {
                                    chapterNameT += String(i)
                                }
                            }
                            if isRecordHua, i == "话" || i == "話" {
                                isRecordHua = false
                                break
                            }
                        }
                        let inpagePathSet = try! FManager.contentsOfDirectory(atPath: chapterURL.path)
                        // 第四次循环,/Users/HUi/usrtmp/bilibili/content/篇*/话*/"页", 获取每一张图片
                        for pageIndex in 0 ..< inpagePathSet.count {
                            let inputPath = chapterPath + "/" + inpagePathSet[pageIndex]
                            // 输出目录
                            //加上“篇“
                            var outRootPath = "/Users/HUi/usrtmp/bilibili/already/" + pianSubPath + "/"
                            if !FManager.fileExists(atPath: outRootPath) {
                                _ = try! runCommand("mkdir", arguments: ["\(outRootPath)"])
                            }
                            //加上”卷“
                            outRootPath += "/" + volSubPath
                            if !FManager.fileExists(atPath: outRootPath) {
                                _ = try! runCommand("mkdir", arguments: ["\(outRootPath)"])
                            }
                            //加上”话“
                            outRootPath += "/" + chapterSubPath
                            if !FManager.fileExists(atPath: outRootPath) {
                               _ = try! runCommand("mkdir", arguments: ["\(outRootPath)"])
                            }
                            //加上“页”
                            let outPath = outRootPath + "/" + "\(chapterNameS)_p\(pageIndex + 1).png" //简体
                            let outPathT = outRootPath + "/" + "\(chapterNameT)_p\(pageIndex + 1).png" //繁体
                            // 开始处理
                            print("########################################")
                            if FManager.fileExists(atPath: outPath) {
                                print("##########FILE ALREADY EXISTED##########")
                                print(outPath)
                            } else if FManager.fileExists(atPath: outPathT) {
                                print("##########FILE ALREADY EXISTED##########")
                                print(outPath)
                                let exeNameChange = try! runCommand("mv", arguments: [outPathT, outPath]).1
                                if exeNameChange == 0 {
                                    print("##########FILE NAME is CHANGED##########")
                                } else {
                                    print("!!!!!!!!!!NAME  CHANGE  FAILED!!!!!!!!!!")
                                }
                            } else {
                                print(inputPath)
                                let exe = try! runCommand("/Users/HUi/bin/waifu2x", arguments: ["--type", "a", "--scale", "2", "--noise", "4", "--input", inputPath, "--output", outPath])
                                print(exe)
                            }
                        }
                    }
                }
            }
        }
    }
}

print("God Bless!")
