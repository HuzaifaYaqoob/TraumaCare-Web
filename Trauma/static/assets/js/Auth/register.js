




const add_error_from_field = (element, error_message) =>{
    let error_parent = element.closest('.form-field')
    if (error_parent){
        let error = error_parent.querySelector('.error-message')
        if (!error){
            error = document.createElement('p')
            error.className = 'error-message'
        }
        console.log(error)
        error.innerHTML = error_message
        error_parent.appendChild(error)

        let error_border = error_parent.querySelector('[error-border-element]')
        if (error_border){
            error_border.classList.add('error')
        }
        
    }
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
                add_error_from_field(element, `User already exist with this ${name}`)
            }
            else{
                remove_error_from_field(element)
            }
        })
    }, 2000);

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

    let error_fields = document.querySelectorAll('.error')
    if (error_fields.length > 0 ){
        alert('Please fix the error above')
        return
    }
    console.log('gonna submit')
}



document.addEventListener('DOMContentLoaded', () =>{
    ValidateUniqueUser()

    let main_register_form = document.querySelector('[main-register-form]')
    if (main_register_form){
        main_register_form.addEventListener('submit' , handleSubmit)
    }
})