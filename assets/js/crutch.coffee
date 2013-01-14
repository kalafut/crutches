this.Crutch = {}
search_split = new RegExp(" +")
$(document).ready () ->
    template = Handlebars.compile(_template)

    $("body").append(template(_data))

    search_hndl = (e) ->
        if e?
            $("#search").val("") if e.keyCode == 27
        val = $("#search").val()
        query = parse_search(val)
        filter(query)
    this.Crutch.filter = search_hndl

    $("#search").on("keyup", search_hndl)

    key("esc", () -> $("#search").focus())

    $(".project_active").on("click", search_hndl)
    filter(parse_search(""))
    $("#search").focus()

    key.filter = () -> return true


hide = (uid) -> $("#" + uid).addClass('hidden')

parse_search = (str) ->
    prj_ind = "/"
    sec_ind = "//"
    terms = []
    projects = []
    sections = []

    for group in str.trim().split(search_split)
        do (group) ->
            if group.indexOf(sec_ind) == 0
                if group.length > sec_ind.length
                    sections.push(group.substring(sec_ind.length))
            else if group.indexOf(prj_ind) == 0
                if group.length > prj_ind.length
                    projects.push(group.substring(prj_ind.length))
            else
                terms.push(group)

    return { terms: terms, projects: projects, sections:sections }

contains = (list, elem) ->
    for e in list
        return true if e == elem
    return false

some = (list, test) ->
    for e in list
        return true if test(e)
    return false

filter = (query) ->
    $(".entry, .section, .project").removeClass("hidden")

    active_projects = $(".project_active:checked")
    active_project_uid = (parseInt $(e).attr("data-uid") for e in active_projects)
    regexes = (new RegExp(e, "i") for e in query.terms)


    for project in _data.projects
        section_found = false
        project_disabled = false

        # If either the project is disabled by the user, or any of the project filters
        # "p:xxx" don't match, mark the project as disabled
        project_disabled = true  if not contains(active_project_uid, project.uid) or (query.projects.length > 0 and some(query.projects, (search) ->
            project.project.toLowerCase().indexOf(search.toLowerCase()) != 0
        ))
        section_idx = 0

        while section_idx < project["sections"].length
            entry_found = false
            section_disabled = false

            # If the section filter "s:xxx" doesn't match, mark the section as disabled
            section_disabled = true  if query.sections.length > 0 and some(query.sections, (search) ->
                project.sections[section_idx].section.toLowerCase().indexOf(search.toLowerCase()) == -1
            )
            entry_idx = 0

            while entry_idx < project["sections"][section_idx]["entries"].length
                entry = project["sections"][section_idx]["entries"][entry_idx]
                matched = true

                # Test each search regex, aborting if any fail to match
                matched = false  if project_disabled or section_disabled or regexes.length > 0 and some(regexes, (re) ->
                    if entry.term?
                        entry.description.search(re) is -1 and entry.term.search(re) is -1 
                    else
                        entry.description.search(re) is -1
                )
                if matched
                    entry_found = true
                    section_found = true
                else
                    $("#" + entry["uid"]).addClass "hidden"
                entry_idx++
            hide project["sections"][section_idx]["uid"]  unless entry_found
            section_idx++
        hide project["uid"]  unless section_found
