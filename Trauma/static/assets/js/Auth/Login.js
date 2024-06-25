

let validation_tm = undefined

const UserValidationApi = (e) =>{
    if (validation_tm){
        clearTimeout(validation_tm)
    }
    let element = e.target
    let parent_form = element.closest('form')
    let button = parent_form.querySelector('button')
    if (button){
        button.disabled = true
    }


    let tm = setTimeout(() => {
        let {value} = element
        if (!value){
            return
        }
        
        let form_data = new FormData()
        form_data.append('mobile_number', value)

        fetch("/api/v1/auth/validate-unique-user/", {method : 'POST', body : form_data}).then(response => response.json()).then(result =>{
            console.log(result.response.reserved_fields)
            if (button){
                button.disabled = false
            }

            let username_field = parent_form.querySelector('[name="username"]')

            if (result?.response?.reserved_fields?.length > 0){
                remove_error_from_field(element)
                if (username_field){
                    username_field.parentElement.classList?.add('hidden')
                    username_field.required = false
                }
            }
            else{
                if (username_field){
                    username_field.parentElement.classList?.remove('hidden')
                    username_field.required = true
                }
            }
        })
    }, 200);

    validation_tm = tm

}


const ValidateUniqueUser = () =>{
    let mobile_field = document.querySelector('[name="mobile_number"]')
    mobile_field.addEventListener('input' , UserValidationApi)
}



const handleSubmit = (e) =>{

    e.preventDefault()
    let form = e.target
    let required_fields = form.querySelectorAll('input[data-required][value=""], input[data-required]:not([value])')
    required_fields = [...required_fields]
    required_fields = required_fields.filter(field => !field.value)

    if (required_fields.length > 0){
        required_fields.forEach(field =>{
            if (!field.value){
                add_error_from_field(field, 'This field is required')
            }
        })
        ShowNotification({type : 'error', message : 'Please fix the error above!'})
        return
    }
    
    let error_fields = form.querySelectorAll('.error')
    if (error_fields.length > 0 ){
        ShowNotification({type : 'error', message : 'Please fix the error above!'})
        return
    }
    ShowNotification({type : 'success', message : 'Submitting, Please wait...!'})
    form.submit()
}


document.addEventListener('DOMContentLoaded', () =>{
    ValidateUniqueUser()
    
    let main_login_form = document.querySelector('[main-login-form]')
    if (main_login_form){
        main_login_form.addEventListener('submit' , handleSubmit)
    }
})