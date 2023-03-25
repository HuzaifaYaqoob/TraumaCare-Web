

let validation_tm = undefined

const UserValidationApi = (e) =>{
    if (validation_tm){
        clearTimeout(validation_tm)
    }

    let tm = setTimeout(() => {
        let element = e.target
        let {name ,value} = element
        if (!value){
            return
        }
        let parent_form = element.closest('.form-field')
        
        let form_data = new FormData()

        if (!name){
            form_data.append('email', value)
            form_data.append('username', value)
            form_data.append('dial_code', value)
            form_data.append('mobile_number', value)
        }
        else{
            form_data.append(name, value)
        }

        fetch("/api/v1/auth/validate-unique-user/", {method : 'POST', body : form_data}).then(response => response.json()).then(result =>{
            console.log(result.response.reserved_fields)
            if (result?.response?.reserved_fields?.length > 0){
                remove_error_from_field(element)
                element.name = result?.response?.reserved_fields[0] ? result?.response?.reserved_fields[0] : ''
            }
            else{
                element.name = ''
                add_error_from_field(element, `User doesn't exist`)
            }
        })
    }, 500);

    validation_tm = tm

}


const ValidateUniqueUser = () =>{
    let input_fields = document.querySelectorAll('[check-user-exist]')
    input_fields.forEach(un_field =>{
        un_field.addEventListener('input' , UserValidationApi)
    })
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