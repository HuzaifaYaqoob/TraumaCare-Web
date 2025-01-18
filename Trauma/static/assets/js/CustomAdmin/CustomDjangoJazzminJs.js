

const head = document.querySelector('head')
let t_script = document.createElement('script')
t_script.src = '/static/assets/tailwind/tailwind.js'
head.appendChild(t_script)


const ShowTopTile = async () =>{
    const current_page = window.location.pathname
    const response = await fetch(`/api/v1/auth/admin/get_custom_admin_top_tiles/?current_page=${current_page}`)
    const result = await response.json()
    if (!result.data){
        return
    }
    let data = result.data
    console.log(data)

    let contentContainer = document.getElementById('content')
    let mainContainer = contentContainer.parentElement
    let TilesDiv = document.createElement('div')
    TilesDiv.className = 'mb-3 grid xl:grid-cols-4 lg:grid-cols-3 md:grid-cols-2 grid-cols-1 gap-[15px]'

    mainContainer.insertBefore(TilesDiv, contentContainer)
    data.forEach(element => {
        let div_html = `
                <div
                    class='bg-white relative flex items-start flex-row !p-5 !pb-2 gap-[11px] rounded-[11px] !border ease-in-out duration-75 cursor-pointer'>
                    <div class='rounded-[6px]'>
                        <i class="!text-[38px] ${element.icon}"></i>
                    </div>

                    <div class="flex !flex-col !font-semibold text-[#626164]">
                    <p class="!text-[18px]">${element.title}</p>
                    <p class="!text-xs font-[400]">${element.desc}</p>
                    <p class="!text-4xl mt-[10px]">${element.value}</p>
                    </div>
                </div>
        `
        TilesDiv.innerHTML += div_html
    });
}

ShowTopTile()