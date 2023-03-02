const showModal = (modalEl, items, opts) => {
    modalEl.on("shown.bs.modal", ()=>{
        if (items.class){
            modalEl.find(".modal-dialog").addClass(items.class);
        };
        if (items.title){
            modalEl.find(".modal-title").text(items.title);
        };
        if (items.body){
            modalEl.find(".modal-body").html(items.body).addClass("col-12");
        }

        if (items.type) {
            let tipe = items.type;
            if (tipe.form){
                const form = document.getElementById(tipe.id);
                form.setAttribute("action", tipe.action)
            }
        };
        console.log(items)
    });
    const opt = opts ? opts : "show";
    modalEl.modal(opt);
}

const xhr = new XMLHttpRequest();

const DataRequest = (method, data_url, data_form) => {
    return new Promise((resolve, reject) => {
        xhr.open(method, data_url, true);
        xhr.setRequestHeader('x-requested-with', 'XMLHttpRequest')

        if (data_form){
            xhr.send(data_form);
        } else {
            xhr.send(null);
        };

        xhr.onload = () => {
            if (xhr.status >= 200){
                resolve(xhr);
            };

            if (xhr.status == 500){
                reject({
                    "err_msg": `Error!: ${xhr.status}`
                })
            }
        }
    })
};

const urlString = (url, value) => {
    const re = /(\/0\/)/;
    const dataUrl = url.replace(re, "/"+value)
    return dataUrl
};

const modalForm = (data)=>{
    const method = data.method ? data.method : "get";
    const response = DataRequest(method, data.url, data.form)
    response.then((items)=>{
        showModal(data.modal, data.items)
    })
}

export {DataRequest};
export {urlString};
export {showModal};
export {modalForm};