$(document).ready(function() {
    $("#prj_all").on("click", function() {
        $(".project_active").prop("checked",true);
        Crutch.filter();
    });
    $("#prj_none").on("click", function() {
        $(".project_active").prop("checked",false);
        Crutch.filter();
    });
});
