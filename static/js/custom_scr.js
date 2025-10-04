var config = null;


$.ajax({
    type: "GET",
    url: "/getConfigBotones",
    success: function (response) {
        config = JSON.parse(response)
        for (let i = 1; i <= 15; i++) {
            var id = "B"+i
            if (config[id] != null) {
                document.querySelector("#"+id).innerHTML = "<div>"+id+"</div><div>"+config[id].accion+"</div>"
            }else{
                document.querySelector("#"+id).innerHTML = "<div>"+id+"</div>"
            }
        }
    }
});




$(".boton").on("click", function () {
    $("#btnID").val(this.id);
    
    if (config[this.id] != null) {
        if (config[this.id].data != null) {
            $("#btnData").val(config[this.id].data);
        }
        document.querySelectorAll("#btnAccion option").forEach((option)=>{
            option.selected = option.value == config[this.id].accion;
        })
    }else{
        document.querySelector("#btnAccion option[value=none]").selected = true
    }
    $("#modalConfiguracionBoton").modal("show")
});


$("#btnGuardarConfiguracionBoton").on("click", function () {

    var data = new FormData()
    data.append("id", $("#btnID").val())
    data.append("accion", $("#btnAccion").val())
    data.append("data", $("#btnData").val())
    $.ajax({
        type: "POST",
        url: "/guardarConfigBoton",
        data: data,
        contentType: false,
        processData: false,
        success: function (response) {
            location.reload()
        }
    });
});



