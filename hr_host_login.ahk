; vm hr host 每日定時重啟後 由此定時登入遠端桌面 
; 獨立運作 不依賴 windows排程

#Singleinstance force ;單線
#Persistent ;持續

Menu, Tray, Icon, desktop2.ico
Menu, Tray, Add, 立即登入, Run_handler
Menu, Tray, Add, 目前狀態, ShowState

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
    SetTitleMatchMode 2
    if WinExist("yshr.asuscomm.com"){
        MsgBox, 64, State, 遠端桌面已連線!, 2
    }
    else{
        ; MsgBox, 64, State, 遠端桌面尚未連線!, 2
        RunWait, C:\Windows\System32\mstsc.exe C:\Users\user\Desktop\yshr.asuscomm.com.rdp
        SetTimer, Restart, -7200000 ; 2小時候重新啟用
    }
    return
}

Restart(){ ;重新啟用
    Global alr
    alr["ready"] := true 
}

ShowState(){
    Global alr
    if(alr["ready"]=1){
        MsgBox, 64, State, Alert is ready, 2
    }
    else{
        MsgBox, 64, State, Alert is not ready, 2
    }
    return
}
