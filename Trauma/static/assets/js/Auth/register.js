



const HandleRegister = () =>{
    
}


let validation_tm = undefined

const UserValidationApi = (e) =>{
    if (validation_tm){
        clearTimeout(validation_tm)
    }

    let tm = setTimeout(() => {
        let element = e.target
        let {name ,value} = element
        let url = element.getAttribute('validation-url')

        let form_data = new FormData()
        form_data.append(name, value)

        fetch(url, {method : 'POST', body : form_data}).then(response => response.json()).then(result =>{
            console.log(result)
        })
    }, 200);

    validation_tm = tm

}


const ValidateUniqueUser = () =>{
    let unique_fields = document.querySelectorAll('[validate-unique-user]')


    unique_fields.forEach(un_field =>{
        un_field.addEventListener('input' , UserValidationApi)
    })
}




document.addEventListener('DOMContentLoaded', () =>{
    ValidateUniqueUser()
})