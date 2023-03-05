


const DropdownField = () =>{
    let drop_fields = document.querySelectorAll('[dropdown]')

    const Togel_DropdownField = (e, dropdown) =>{
        dropdown.classList.toggle('hidden')
    }
    
    if (drop_fields.length > 0){
        drop_fields.forEach(field =>{
            let dropdown = field.parentElement.querySelector('[dropdown-data]')
            if (dropdown) {
                field.addEventListener('click' ,(e) => Togel_DropdownField(e, dropdown))
            }
            else{
                console.log(dropdown)
            }
        })
    }
}



const StartScript = () =>{
    DropdownField()
}


document.addEventListener('DOMContentLoaded' , StartScript)