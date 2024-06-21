


const ShowHideChatWidget = () =>{
    let chat_widget = document.querySelector('[MainChatWidgetChatBot]')
    if (chat_widget){
        chat_widget.classList.toggle('hidden')
        scrollToBottom()
    }

    if (chat_widget.className.includes('hidden')){
        localStorage.removeItem('showChatWidget')
    }
    else{
        localStorage.setItem('showChatWidget', true)
    }
}

let messagesMain = document.querySelector('[MainChatWidgetChatMessages]')
let MsgNotificationSound = document.querySelector('[MsgNotificationSound]')
let chat_id = document.querySelector('[UserAIBotChatWidgetChatId]')
chat_id = chat_id ? chat_id.value : undefined


const getMessageContent = (message, isMe=false) =>{
    if (!isMe){
        messagesMain?.querySelector('.loader')?.closest('[ChatWidgetChatMessage]')?.remove()
    }
    let div = document.createElement('div')
    div.setAttribute('ChatWidgetChatMessage', '')
    div.className = `flex items-start w-full gap-3 ${isMe ? 'user-message' : 'ai-bot-message'} `
    let content = `${isMe ? '' : `<img class="w-[30px] border rounded-full h-auto" src="/static/assets/Images/bot-icon.jpeg" />`}
        <div class="flex-1 w-full">
            <p class="chat-message px-3 mb-1.5 py-2 bg-[#eff1f4] w-max max-w-[70%] font-[500]">${message.replace('\n', '<br/>')}</p>
        </div>`
    
    div.innerHTML = content
    return div
}
const Loader = () =>{
    let div = document.createElement('div')
    div.setAttribute('ChatWidgetChatMessage', '')
    div.className = `flex items-center w-full gap-3 ai-bot-message`
    let content = `<img class="w-[30px] border rounded-full h-auto" src="/static/assets/Images/bot-icon.jpeg" />
        <div class="flex-1 w-full">
            <div class="loader ml-6"></div>
        </div>`
    
    div.innerHTML = content
    return div
}

const scrollToBottom = () =>{
    messagesMain.scrollTop = messagesMain.scrollHeight
}

const handlePredefinedMessageClick = (element, autoSubmit=true) =>{
    let message = ''
    let message_el = element.querySelector('[preDefinedMessage]')
    if (message_el){
        message = message_el.getAttribute('preDefinedMessage')
    }
    let textarea = document.querySelector('[MainChatWidgetChatBot] textarea')
    textarea.value = message
    if (autoSubmit){
        onSubmitChatWidget()
    }
    else{
        textarea.focus()
    }
}

const onSubmitChatWidget = async () =>{
    if (!chat_id){
        chat_id = document.querySelector('[UserAIBotChatWidgetChatId]')
    }
    let prev_messages = messagesMain.querySelectorAll('[ChatWidgetChatMessage]')
    if (prev_messages.length == 0){
        messagesMain.innerHTML = ''
    }
    let textarea = document.querySelector('[MainChatWidgetChatBot] textarea')
    messagesMain.appendChild(getMessageContent(textarea.value, true))
    messagesMain.appendChild(Loader()) // Loading...
    scrollToBottom()
    let value = textarea.value
    textarea.value = ''
    console.log(textarea.value)

    let response = await fetch(`/api/v1/chatxpo/send_chat_widget_message/${chat_id}/`, {
        body : JSON.stringify({
            query : value
        }),
        method : 'POST',
        headers : {
            'Content-Type' : 'application/json'
        }
    })
    response = await response.json()
    let message = response.response.message
    console.log(message)
    messagesMain.appendChild(getMessageContent(message))
    scrollToBottom()
    if (MsgNotificationSound){
        MsgNotificationSound.play()
    }
}

document.addEventListener('DOMContentLoaded', () =>{
    if (localStorage.getItem('showChatWidget')){
        ShowHideChatWidget()
    }
    let bot_icons = document.querySelectorAll('.chatWidgetBotIcon')
    bot_icons.forEach(bot_icon =>{
        bot_icon.addEventListener('click', ShowHideChatWidget)
    })

    let send_button = document.querySelector('[ChatWidgetSubmitButton]')
    if (send_button){
        send_button.addEventListener('click', onSubmitChatWidget)
    }

    let textarea = document.querySelector('[MainChatWidgetChatBot] textarea')
    if (textarea){
        textarea.addEventListener('keydown', (e) =>{
            if (e.key === 'Enter' && e.shiftKey){
                e.preventDefault()
                onSubmitChatWidget()
            }
        })
    }

    if (MsgNotificationSound){
        MsgNotificationSound.volume = 0.5
    }
    scrollToBottom()
})