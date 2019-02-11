$("#btn-request").click(
    function () {
        
        const END_POINTS_URL = [
            "list_car",
            "list_car_by_user",
            "list_car_by_brand",
            "get_car_count_by_brand"
        ]
        let endpoint = $("#select-endpoint").val();
        let param = $("#param").val() !== "" ? $("#param").val() : "";
        let selectedEndpoint = END_POINTS_URL[endpoint];
        $("#display-result").val("");
        function buildURL(selectedEndpoint, param = "") {
            if (param == "") {
                return "/" + selectedEndpoint;
            } else {
                return "/" + selectedEndpoint + "/" + param;
            }
        }
        let url = buildURL(selectedEndpoint, param);
        console.log(url);
        $.ajax({
            type: "GET",
            url: url,
            success: function (response) {
                let responseText = JSON.stringify(response, null, "\t");
                $("#display-result").val(responseText);
            }
        });

    }
);