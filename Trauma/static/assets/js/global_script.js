document.addEventListener('DOMContentLoaded' , ()=>{
    let all_included = document.querySelectorAll('[data-include]')
    all_included.forEach(incl_div =>{
        let path = incl_div.getAttribute('data-include')
        incl_div.innerHTML = ''

        fetch(
            'Components/Header.html'
        ).then(response => response.text()).then(content =>{
            incl_div.innerHTML = content
        })

    })
})