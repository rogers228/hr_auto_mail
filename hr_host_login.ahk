; vm hr host 每日定時重啟後 由此定時登入遠端桌面 
; 獨立運作 不依賴 windows排程

#Singleinstance force ;單線
#Persistent ;持續
Menu, Tray, Icon, desktop2.ico
SetTimer, Alert_handler, 1000
alr := {"ready": true, "show_clock": false, "h":1, "m":30, "s":0}

Alert_handler(){
    Global alr
    if (alr["show_clock"] = true){
        ToolTip, %A_Hour%:%A_Min%:%A_Sec%
    }

    if (alr["ready"] = true  and A_Hour = alr["h"] and A_Min = alr["m"]){
        ; 時間到
        alr["ready"] := false ;停用
        ToolTip
        Run_handler() ;執行
    }
}

Run_handler(){
    ; 登入遠端桌面 hr host
    RunWait, C:\Windows\System32\mstsc.exe C:\Users\user\Desktop\yshr.asuscomm.com.rdp
    SetTimer, Restart, -7200000 ; 2小時候重新啟用
}

Restart(){ ;重新啟用
    Global alr
    alr["ready"] := true 
}