


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
            coords.forEach((coord, coo_i) =>{
                let loc_coords = coord.getAttribute('ShowDistance')
                if (loc_coords){
                    location_coords[`${loc_coords}`] = loc_coords
                }
            })
            const response = await fetch('/api/v1/get_location_distance/', {
                method : 'POST',
                headers : {
                    'Content-Type': 'application/json'
                },
                body : JSON.stringify({"my_coords" : {'lat' : user_location[0],'lng' : user_location[1],},'location_coords' : location_coords})
            })
            let result = await response.json()
            for (let key in result){
                let ltn_key = location_coords[key]
                let elements = document.querySelectorAll(`[ShowDistance="${ltn_key}"]`)
                elements.forEach(element => {
                    element.innerHTML = `(${result[key]} Km)`
                    let a = `<a target="_blank" href="https://www.google.com/maps/dir/?api=1&origin=${user_location[0]},${user_location[1]}&destination=${key}" class="whitespace-nowrap underline">Get Directions</a>`
                    element.parentElement.innerHTML += a
                })
            }
        }
    }
}

function setCookie(c_name, value, exdays) {
    var exdate = new Date();
    exdate.setDate(exdate.getDate() + exdays);
    var c_value = escape(value) + 
        ((exdays == null) ? "" : "; expires=" + exdate.toUTCString()) + 
        "; path=/"; // Ensure cookie is available for the entire domain
    document.cookie = c_name + "=" + c_value;
}

function getCookie(c_name) {
    var i, x, y, ARRcookies = document.cookie.split(";");
    for (i = 0; i < ARRcookies.length; i++) {
        x = ARRcookies[i].substr(0, ARRcookies[i].indexOf("="));
        y = ARRcookies[i].substr(ARRcookies[i].indexOf("=") + 1);
        x = x.replace(/^\s+|\s+$/g, "");
        if (x == c_name) {
            return unescape(y);
        }
    }
}

let KEYS = {
    "subtotal" : 'Subtotal',
    "discount_applied" : 'Discount Applied',
    "platform_fee" : 'Platform Fee',
    "delivery_charges" : 'Delivery Charges',
    "grand_total" : 'Grand Total',
}

const ClearCart = () =>{
    let CartItems = getCookie('CartItems')
    if (CartItems){
        setCookie('CartItems', '', 1)
    }
    // reload Page 
    window.location.reload()
}

const removeItemFromCart = (p_id) =>{
    console.log(p_id)
    let CartItems = getCookie('CartItems');
    if (CartItems){
        CartItems = JSON.parse(CartItems)
        CartItems = CartItems.filter(itm => itm.p_id != p_id)
        setCookie('CartItems', JSON.stringify(CartItems), 7)
    }
    showSidebarCart(true)
}

function add_to_cart_btn(productId, location_stock, ProductQuantity) {
    console.log(productId, location_stock, ProductQuantity)
    if (!ProductQuantity) {
        ProductQuantity = document.querySelector('[ProductQuantity]').getAttribute('ProductQuantity');
    }

    if (!ProductQuantity){
        ProductQuantity = 1
    }
    let CartItems = getCookie('CartItems');
    if (CartItems){
          CartItems = JSON.parse(CartItems)
    }
    else{
          CartItems = []
    }
    let already_exist = CartItems.find(item => item.id == productId)
    if (already_exist){
        CartItems = CartItems.map(itm => ({...itm, 'location_stock' : location_stock, quantity : itm.id == productId ? parseInt(ProductQuantity) : parseInt(itm.quantity),}))
    }
    else{
        CartItems.push({'id' : productId, 'quantity' : ProductQuantity, 'location_stock' : location_stock})
    }
    setCookie('CartItems', JSON.stringify(CartItems), 7)
    ShowNotification({type : 'success', message : 'Cart updated successfully'})
    setTimeout(() => {
          showSidebarCart()
    }, 1000);
  }

const showSidebarCart = async (stillUpdate) => {
    let CartItems = getCookie('CartItems');
    if (CartItems){
        CartItems = JSON.parse(CartItems)
    }

    if (CartItems.length == 0 && !stillUpdate){
        return
    }

    const response = await fetch('/api/v1/product/calculate_cart/', {method : 'POST'})
    const result = await response.json()
    console.log(result)
    if (result?.data.length == 0 && !stillUpdate) {
        return
    }
    let CartItems_div = document.querySelector('[CartItems]')
    CartItems_div.innerHTML = ''
    result?.data?.forEach((prod_itm) => {
        console.log(prod_itm)

        // <a href="/product/view/${prod_itm.slug}/?selected_location=${prod_itm.location_id}" class="max-w-[120px] w-full h-24 flex items-center justify-center">
        //         <img src="${prod_itm.image}" alt="${prod_itm.name}">
        // </a>
        // <div class="flex items-center gap-1">                      
        //     ${prod_itm.discount ?  `<span class="text-xs text-[#3C3C3C]/60"><del>Rs.${prod_itm.price}</del></span>` : ''}
        //     <p class="text-[#05D57C] outfit-font font-semibold italic"><span class="font-medium text-[#151E2C] text-xs">Rs.</span>${prod_itm.final_price}</p>
        // </div>
        // <div class="flex items-center justify-between gap-1">
        //     <div class="flex items-center rounded-md bg-[#6C7793] w-[100px] h-[30px] p-[1px]">
        //             <button class="cursor-pointer text-white font-semibold flex-1 h-full flex items-center justify-center">-</button>
        //             <p class="text-[#0A1C4B] font-semibold rounded-md flex-1 h-full flex bg-white items-center justify-center outfit-font">${prod_itm.quantity}</p>
        //             <button class="cursor-pointer text-white font-semibold flex-1 h-full flex items-center justify-center">+</button>
        //     </div>
            // <span class="flex items-center justify-center size-6 cursor-pointer">
            //         <svg class="size-4 fill-black/50" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M135.2 17.7C140.6 6.8 151.7 0 163.8 0L284.2 0c12.1 0 23.2 6.8 28.6 17.7L320 32l96 0c17.7 0 32 14.3 32 32s-14.3 32-32 32L32 96C14.3 96 0 81.7 0 64S14.3 32 32 32l96 0 7.2-14.3zM32 128l384 0 0 320c0 35.3-28.7 64-64 64L96 512c-35.3 0-64-28.7-64-64l0-320zm96 64c-8.8 0-16 7.2-16 16l0 224c0 8.8 7.2 16 16 16s16-7.2 16-16l0-224c0-8.8-7.2-16-16-16zm96 0c-8.8 0-16 7.2-16 16l0 224c0 8.8 7.2 16 16 16s16-7.2 16-16l0-224c0-8.8-7.2-16-16-16zm96 0c-8.8 0-16 7.2-16 16l0 224c0 8.8 7.2 16 16 16s16-7.2 16-16l0-224c0-8.8-7.2-16-16-16z"/></svg>
            // </span>
        // </div>
        let product_card = `
                <div class="flex items-center gap-3 border-b border-[#CACBE6] py-2">
                        <div class="flex-1 space-y-1">
                            <div class='flex items-start justify-between gap-1'>
                                <div class=''>
                                    <a href="/product/view/${prod_itm.slug}/?selected_location=${prod_itm.location_id}" class="font-medium text-sm outfit-font line-clamp-2 text-[#151E2C] line-clamp-1">${prod_itm.name}</a>
                                    <div class="text-[#FFFFFF] text-[10px] bg-[#F01275] max-w-max rounded-full px-2.5 py-[3px] line-clamp-1 outfit-font">${prod_itm.store_name}</div>
                                </div>
                                <div>
                                    <div class='flex gap-2 items-center whitespace-nowrap'>
                                        ${prod_itm.discount ?  `<span class="text-xs text-[#3C3C3C]/60 whitespace-nowrap"><del>Rs.${prod_itm.price}</del></span>` : ''}
                                        <p class="text-[#05D57C] outfit-font font-semibold italic whitespace-nowrap"><span class="font-medium text-[#151E2C] text-xs">Rs.</span>${prod_itm.final_price}</p>
                                        <span class='outfit-font whitespace-nowrap text-xs'>X ${prod_itm.quantity}</span>
                                    </div>
                                    <span onclick="removeItemFromCart('${prod_itm.id}')" class="ml-auto flex items-center justify-center size-6 cursor-pointer">
                                        <svg class="size-4 fill-black/50" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M135.2 17.7C140.6 6.8 151.7 0 163.8 0L284.2 0c12.1 0 23.2 6.8 28.6 17.7L320 32l96 0c17.7 0 32 14.3 32 32s-14.3 32-32 32L32 96C14.3 96 0 81.7 0 64S14.3 32 32 32l96 0 7.2-14.3zM32 128l384 0 0 320c0 35.3-28.7 64-64 64L96 512c-35.3 0-64-28.7-64-64l0-320zm96 64c-8.8 0-16 7.2-16 16l0 224c0 8.8 7.2 16 16 16s16-7.2 16-16l0-224c0-8.8-7.2-16-16-16zm96 0c-8.8 0-16 7.2-16 16l0 224c0 8.8 7.2 16 16 16s16-7.2 16-16l0-224c0-8.8-7.2-16-16-16zm96 0c-8.8 0-16 7.2-16 16l0 224c0 8.8 7.2 16 16 16s16-7.2 16-16l0-224c0-8.8-7.2-16-16-16z"/></svg>
                                    </span>
                                </div>
                            </div>
                        </div>
                  </div>
            `
        CartItems_div.innerHTML =  CartItems_div.innerHTML + product_card

    })

    
    let CartBottomBillingBar = document.querySelector('[CartBottomBillingBar]')
    CartBottomBillingBar.innerHTML = ''
    if (CartBottomBillingBar){
        [
            "grand_total",
            "delivery_charges",
            "platform_fee",
            "discount_applied",
            "subtotal",
        ].forEach((key) => {
            let val = result[key]
            let elmnt = `
                    <div class="flex items-center justify-between py-2 border-b border-[#CACBE6]">
                        <h4 class="text-[${key == 'discount_applied' ? '#0555E9' : '#151E2C'}] outfit-font font-medium text-sm">${KEYS[key]}:</h4>
                        <p class="text-[${key == 'discount_applied' ? '#0555E9' : '#151E2C'}] outfit-font font-medium text-sm">Rs.${(key == 'discount_applied' && val) ? ' -' : ''}${val}</p>
                    </div>
            `
            CartBottomBillingBar.innerHTML = elmnt + CartBottomBillingBar.innerHTML
        })
    }

    


    let cart__popup__main = document.getElementById('cart__popup__main');
    let cart__popup__main__width = document.getElementById('cart__popup__main__width');

    cart__popup__main?.classList.add('!block');
    cart__popup__main__width?.classList.add('w-full');

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