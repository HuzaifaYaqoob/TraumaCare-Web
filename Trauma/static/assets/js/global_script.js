


const remove_error_from_field = (element) =>{
    let error_parent = element.closest('.form-field')
    if (error_parent){
        let error = error_parent.querySelector('.error-message')
        let error_border = error_parent.querySelector('[error-border-element]')
        if (error_border){
            error_border.classList.remove('error')
        }
        if (error){
            error.remove()
        }
    }
}


const add_error_from_field = (element, error_message) =>{
    let error_parent = element.closest('.form-field')
    if (error_parent){
        let error = error_parent.querySelector('.error-message')
        if (!error){
            error = document.createElement('p')
            error.className = 'error-message'
        }
        error.innerHTML = error_message
        error_parent.appendChild(error)

        let error_border = error_parent.querySelector('[error-border-element]')
        if (error_border){
            error_border.classList.add('error')
        }
        
    }
}


const check_password_strong = (password) =>{
    var strength = 0;

    if (+password.length < 8){
        strength = 0
        return strength
    }
    else{
        return 8
    }

    // if (password.match(/[a-z]+/)) {
    //     strength += 1;
    // }
    // if (password.match(/[A-Z]+/)) {
    //     strength += 1;
    // }
    // if (password.match(/[0-9]+/)) {
    //     strength += 1;
    // }
    // if (password.match(/[$@#&!]+/)) {
    //     strength += 1;
    // }

    return strength
}


const DropdownField = () =>{
    let drop_fields = document.querySelectorAll('[dropdown]')

    const Togel_DropdownField = (e, dropdown) =>{
        dropdown.classList.toggle('hidden')
    }

    const handle_dropdown_search_input = (e) =>{
        let search_text = e.target.value
        let parent_dropdown = e.target.closest('.dropdown-data')
        let dropdown_items = parent_dropdown.querySelectorAll('.dropdown-items [data-search]')
        dropdown_items.forEach(dropdown_item =>{
            let search_value = dropdown_item.getAttribute('data-search')
            if (search_value){
                search_value = search_value.toLowerCase()
                if (search_value.includes(search_text.toLowerCase())){
                    dropdown_item.parentElement.classList.remove('hidden')
                }
                else{
                    dropdown_item.parentElement.classList.add('hidden')
                }
            }
        })
    }

    const handle_click_dropdown_item = (e) =>{
        let element = e.currentTarget
        remove_error_from_field(element)
        let parent_dropdown = element.closest('[dropdown-main-component]')
        let value_field = parent_dropdown.querySelector('[dropdown-field]')
        let value_display = parent_dropdown.querySelector('[dropdown-value-display]')

        let display_value = element.getAttribute('display-value')
        let value = element.getAttribute('value')
        value_field.value = value
        if (display_value){
            value_display.innerHTML = ``
            if (display_value == 'SELF'){
                let new_element = element.cloneNode(true)
                new_element.style.padding = '0'
                value_display.appendChild(new_element)
            }
            else{
                value_display.innerHTML = display_value
            }
        }
        let dropdown_data = parent_dropdown.querySelector('[dropdown-data]')
        if (dropdown_data){
            dropdown_data.classList.add('hidden')
        }
    }
    
    if (drop_fields.length > 0){
        drop_fields.forEach(field =>{
            let dropdown_data = field.parentElement.querySelector('[dropdown-data]')
            if (dropdown_data) {
                field.addEventListener('click' ,(e) => Togel_DropdownField(e, dropdown_data))
                let data_search_field = dropdown_data.querySelector('.dropdown-search-field input[search-field]')
                if (data_search_field){
                    data_search_field.addEventListener('input', handle_dropdown_search_input)
                }

                let dropdown_items = dropdown_data.querySelectorAll('.dropdown-items [data-search]')
                dropdown_items.forEach(drp_itm =>{
                    drp_itm.addEventListener('click', handle_click_dropdown_item, false)
                })
            }
        })
    }
}

const BodyClicked = () =>{
    let body = document.querySelector('body')
    if (body){

    }

}

const OnInputRemoveErrors = () =>{
    let inputs = document.querySelectorAll('input')
    inputs.forEach(inpt =>{
        inpt.addEventListener('input' , (e) => remove_error_from_field(e.target))
    })
}

const handleStarSelect = (e, index, path) =>{
    let thisPath = e.currentTarget
    let pathParentRatingDiv = thisPath.closest('[RatingStars]')
    if (pathParentRatingDiv){
        let input = pathParentRatingDiv.querySelector('[ratingInput]')
        if (input){
            input.value = index + 1
        }
    }
    path.forEach((path, p_index) =>{
        if (p_index <= index){
            path.style.fill = '#FEB546'
        }
        else{
            path.style.fill = '#A7A7A7'
        }
        path.style.opacity = 1
    })
}

const handlePasswordShowOrHide = () =>{
    let showOrHidePasswordCheckBoxs = document.querySelectorAll('[showOrHidePasswordCheckBox]')
    showOrHidePasswordCheckBoxs.forEach(checkbox =>{
        let thisCheckBox = checkbox
        let parentForm = thisCheckBox.closest('form')
        if (!parentForm){
            console.log('parentForm not found')
            return 
        }
        let passwordFields = parentForm.querySelectorAll('[passwordField]')
        checkbox.addEventListener('click', (event)=>{
            passwordFields.forEach(password_field =>{
                if (password_field.type == 'text'){
                    password_field.type = 'password'
                }
                else{
                    password_field.type = 'text'
                }
            })
        })
    })
}

const accessLocation = async () => {
    if (navigator.geolocation) {
        return new Promise((resolve, reject) => {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    const latitude = position.coords.latitude;
                    const longitude = position.coords.longitude;
                    resolve([latitude, longitude]); // Resolve the promise with lat and long
                },
                (error) => {
                    reject(error); // Reject the promise if there's an error
                }
            );
        });
    } else {
        throw new Error('Geolocation is not supported by this browser');
    }
};

// https://www.google.com/maps/dir/?api=1&origin=31.5162624,74.3112704&destination=31.48372354559183,74.28036546591997

const ShowDistances = async () =>{
    let coords = document.querySelectorAll('[ShowDistance]')
    if (coords.length > 0){
        const user_location = await accessLocation()
        if (user_location){
            const location_coords = {}
            coords.forEach(coord =>{
                let loc_coords = coord.getAttribute('ShowDistance')
                location_coords[loc_coords] = loc_coords
            })
            const response = await fetch('/api/v1/get_location_distance/', {
                method : 'POST',
                headers : {
                    'Content-Type': 'application/json'
                },
                body : JSON.stringify({"my_coords" : {'lat' : user_location[0],'lng' : user_location[1],},'location_coords' : location_coords})
            })
            let result = await response.json()
            console.log(result)
            for (let key in result){
                let element = document.querySelector(`[ShowDistance="${key}"]`)
                if (element){
                    element.innerHTML = `(${result[key]} Km)`
                    let a = `<a target="_blank" href="https://www.google.com/maps/dir/?api=1&origin=${user_location[0]},${user_location[1]}&destination=${key}" class="whitespace-nowrap underline">Get Directions</a>`
                    element.parentElement.innerHTML += a
                }
            }
        }
    }
}

const StartScript = () =>{
    // accessLocation()
    BodyClicked()
    DropdownField()
    ShowDistances()

    OnInputRemoveErrors()


    const stars = document.querySelectorAll('[RatingStars] svg')
    stars.forEach((star_svg, index) =>{
        let starParent = star_svg.closest('[RatingStars]')
        let paths = starParent.querySelectorAll('svg path')
        star_svg.addEventListener('click', (e) => handleStarSelect(e, index, paths))
    })

    handlePasswordShowOrHide()
}

document.addEventListener('DOMContentLoaded' , StartScript)