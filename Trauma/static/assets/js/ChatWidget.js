


const ShowHideChatWidget = () =>{
    let chat_widget = document.querySelector('[MainChatWidgetChatBot]')
    if (chat_widget){
        chat_widget.classList.toggle('hidden')
    }
}

document.addEventListener('DOMContentLoaded', () =>{
    let bot_icon = document.querySelector('[MainChatWidgetChatBotIcon]')
    if (bot_icon){
        bot_icon.addEventListener('click', ShowHideChatWidget)
    }
})