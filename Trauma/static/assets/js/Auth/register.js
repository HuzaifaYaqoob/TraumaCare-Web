




let validation_tm = undefined

const UserValidationApi = (e) =>{
    if (validation_tm){
        clearTimeout(validation_tm)
    }

    let tm = setTimeout(() => {
        let element = e.target
        let {name ,value} = element
        let url = element.getAttribute('validation-url')
        let parent_form = element.closest('.form-field')

        
        let form_data = new FormData()

        let combine_field = element.hasAttribute('combine-field')
        if (combine_field){
            let cmb_field_name = element.getAttribute('combine-field')
            combine_field = parent_form.querySelector(`[name="${cmb_field_name}"]`)
        }
        if (combine_field){
            form_data.append(combine_field.name, combine_field.value)
        }

        form_data.append(name, value)

        fetch(url, {method : 'POST', body : form_data}).then(response => response.json()).then(result =>{
            console.log(result.response.reserved_fields)
            if (result?.response?.reserved_fields?.length > 0){
                if (!result?.response?.reserved_fields?.includes('mobile_number')){
                    let form = element.closest('form')
                    let username = form.querySelector('[name="username"]')
                    if (username){
                        username.closest('[usernameFieldParent]')?.classList.remove('hidden')
                    }
                }
                add_error_from_field(element, `User already exist with this ${name}`)
            }
            else{
                remove_error_from_field(element)
            }
        })
    }, 500);

    validation_tm = tm

}


const ValidateUniqueUser = () =>{
    let unique_fields = document.querySelectorAll('[validate-unique-user]')
    unique_fields.forEach(un_field =>{
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

    let phn_field = form.querySelector('[name="mobile_number"]')
    if (phn_field){
        if (phn_field.value.length != 11 || !phn_field.value.startsWith('03')){
            add_error_from_field(phn_field, 'Enter a valid phone number')
        }
    }

    let psword = form.querySelector('[name="password"]')
    if (psword){
        if (check_password_strong(psword.value) < 4){
            // add_error_from_field(psword, 'Please enter strong password')
            add_error_from_field(psword, 'Be at least 8 characters.')
            ShowNotification({type : 'error', message : 'Be at least 8 characters.!'})
            return
        }
        let cnf_password = form.querySelector('[name="confirm_password"]')
        if (psword.value != cnf_password.value){
            add_error_from_field(psword, 'Password does not match')
            add_error_from_field(cnf_password, 'Password does not match')
            ShowNotification({type : 'error', message : 'Password does not match!'})
            return
        }
    }

    let error_fields = form.querySelectorAll('.error')
    if (error_fields.length > 0 ){
        ShowNotification({type : 'error', message : 'Please fix the error above!'})
        return
    }
    ShowNotification({type : 'success', message : 'Submitting, Please wait...!'})
    form.submit()
}


const strongPassword = (form) =>{
    let password_field = form.querySelector('[type="password"][strong_password]')
    let field = undefined
    let bars = undefined
    if (password_field){
        password_field.addEventListener('input' , (e)=>{
            if (!field){
                field = password_field.closest('.form-field')
            }
            if (!bars){
                bars = field.querySelectorAll('.password-bar')
                bars = [...bars]
            }

            bars.forEach(bar =>{
                bar.classList.remove('bg-green-600')
            })

            let strong = check_password_strong(e.target.value)
            let ft_bars = bars.slice(0, strong)
            ft_bars.forEach(bar =>{
                bar.classList.add('bg-green-600')
            })
            console.log(ft_bars.length)
        })
    }
}

document.addEventListener('DOMContentLoaded', () =>{
    ValidateUniqueUser()
    
    let main_register_form = document.querySelector('[main-register-form]')
    if (main_register_form){
        main_register_form.addEventListener('submit' , handleSubmit)
        strongPassword(main_register_form)
    }
})