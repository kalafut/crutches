$(document).ready(function() {
    $("#prj_all").on("click", function() {
        $(".project_active").prop("checked",true);
        Ragbag.filter();
    });
    $("#prj_none").on("click", function() {
        $(".project_active").prop("checked",false);
        Ragbag.filter();
    });
});
