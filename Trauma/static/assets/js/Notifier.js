

let NOTIFIER_ICONS = {
    'success' : '<svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M10 0C4.5 0 0 4.5 0 10C0 15.5 4.5 20 10 20C15.5 20 20 15.5 20 10C20 4.5 15.5 0 10 0ZM8 15L3 10L4.41 8.59L8 12.17L15.59 4.58L17 6L8 15Z" fill="white"/></svg>',
    'error' : '<svg width="20" height="18" viewBox="0 0 20 18" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M2.09977 17.8437H17.9002C19.5159 17.8437 20.5231 16.0916 19.7153 14.6962L11.8151 1.04654C11.0072 -0.348848 8.9928 -0.348848 8.18494 1.04654L0.284714 14.6962C-0.523145 16.0916 0.484055 17.8437 2.09977 17.8437ZM10 10.4995C9.42296 10.4995 8.95083 10.0274 8.95083 9.45037V7.35204C8.95083 6.775 9.42296 6.30287 10 6.30287C10.577 6.30287 11.0492 6.775 11.0492 7.35204V9.45037C11.0492 10.0274 10.577 10.4995 10 10.4995ZM11.0492 14.6962H8.95083V12.5979H11.0492V14.6962Z" fill="white"/></svg>',
    'info' : '<svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M10 0C8.02219 0 6.08879 0.58649 4.4443 1.6853C2.79981 2.78412 1.51809 4.3459 0.761209 6.17316C0.00433284 8.00042 -0.1937 10.0111 0.192152 11.9509C0.578004 13.8907 1.53041 15.6725 2.92894 17.0711C4.32746 18.4696 6.10929 19.422 8.0491 19.8078C9.98891 20.1937 11.9996 19.9957 13.8268 19.2388C15.6541 18.4819 17.2159 17.2002 18.3147 15.5557C19.4135 13.9112 20 11.9778 20 10C19.9975 7.34861 18.9431 4.80655 17.0683 2.93174C15.1934 1.05693 12.6514 0.00254574 10 0ZM9.80769 4.61538C10.0359 4.61538 10.259 4.68306 10.4487 4.80984C10.6385 4.93663 10.7864 5.11683 10.8737 5.32767C10.961 5.53851 10.9839 5.77051 10.9394 5.99433C10.8948 6.21816 10.785 6.42375 10.6236 6.58512C10.4622 6.74649 10.2566 6.85638 10.0328 6.9009C9.80897 6.94543 9.57697 6.92258 9.36614 6.83524C9.1553 6.74791 8.97509 6.60002 8.84831 6.41027C8.72152 6.22052 8.65385 5.99744 8.65385 5.76923C8.65385 5.46321 8.77541 5.16973 8.9918 4.95334C9.20819 4.73695 9.50168 4.61538 9.80769 4.61538ZM10.7692 15.3846H10C9.79599 15.3846 9.60033 15.3036 9.45607 15.1593C9.31182 15.0151 9.23077 14.8194 9.23077 14.6154V10C9.02676 10 8.8311 9.91895 8.68684 9.7747C8.54258 9.63044 8.46154 9.43478 8.46154 9.23077C8.46154 9.02675 8.54258 8.8311 8.68684 8.68684C8.8311 8.54258 9.02676 8.46154 9.23077 8.46154H10C10.204 8.46154 10.3997 8.54258 10.5439 8.68684C10.6882 8.8311 10.7692 9.02675 10.7692 9.23077V13.8462C10.9732 13.8462 11.1689 13.9272 11.3132 14.0715C11.4574 14.2157 11.5385 14.4114 11.5385 14.6154C11.5385 14.8194 11.4574 15.0151 11.3132 15.1593C11.1689 15.3036 10.9732 15.3846 10.7692 15.3846Z" fill="white"/></svg>',
    'warning' : '<svg width="20" height="18" viewBox="0 0 20 18" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M2.09977 17.8437H17.9002C19.5159 17.8437 20.5231 16.0916 19.7153 14.6962L11.8151 1.04654C11.0072 -0.348848 8.9928 -0.348848 8.18494 1.04654L0.284714 14.6962C-0.523145 16.0916 0.484055 17.8437 2.09977 17.8437ZM10 10.4995C9.42296 10.4995 8.95083 10.0274 8.95083 9.45037V7.35204C8.95083 6.775 9.42296 6.30287 10 6.30287C10.577 6.30287 11.0492 6.775 11.0492 7.35204V9.45037C11.0492 10.0274 10.577 10.4995 10 10.4995ZM11.0492 14.6962H8.95083V12.5979H11.0492V14.6962Z" fill="white"/></svg>',
}

let cross_icon = '<svg width="12" height="12" viewBox="0 0 12 12" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M1 11L11 1M1 1L11 11" stroke="#6A727D" stroke-width="2" stroke-linecap="round"/></svg>'


const ShowNotification = (data) =>{
    let main_tc_notifiers = document.querySelector('[main-tc-notifiers]')

    let notifier = document.createElement('div')
    notifier.className = 'tc-notifier sliding-roll'
    notifier.classList.add(data.type)


    let icon = document.createElement('div')
    icon.classList.add('icon')
    icon.innerHTML = NOTIFIER_ICONS[data.type]
    notifier.appendChild(icon)


    let message = document.createElement('div')
    message.classList.add('msg')
    message.innerHTML = data.message
    notifier.appendChild(message)


    let cross = document.createElement('span')
    cross.classList.add('cross')
    cross.innerHTML = cross_icon
    cross.addEventListener('click', () =>{
        notifier.classList.add('sliding-reverse-roll')
        setTimeout(() => {
            notifier.remove()
        }, 300);
    })
    notifier.appendChild(cross)

    let total_notifications = main_tc_notifiers.querySelectorAll('.tc-notifier')
    console.log(total_notifications)
    if (total_notifications.length >= 7){
        total_notifications[0]?.remove()
    }


    main_tc_notifiers.appendChild(notifier)
}

document.addEventListener('DOMContentLoaded' , () =>{

})