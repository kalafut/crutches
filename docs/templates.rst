.. _templates:

Template Guide
##############

Templates allow complete flexibility in how content is presents and even acted upon. The `crutch` parser will provide the template
with virtually all of the input data (after being massaged and filter based on configuration), and it's up to the template logic to
display it. This arrangement makes it easy to customized the output to your liking, or come up with an entirely different scheme altogether.

It is important to first understand the steps taken to parse and prepare the template:

1. The template file specified by the configuration is loaded.
2. References to external JavaScript and stylesheets are located
3. Scripts and stylesheets from the `assets` directory (and below) are loaded. Compilation will fail if they're not found.
4. External script and stylesheet tags are replaced with the actual file contents.
5. Everything within the templates `<body>` tag is *moved* into a JavaScrip variable.
6. All reference content is placed in a JavaScript.
7. The Crutch.render() function is called, which should populate the template with ref card data, and target the result back in the `<body` section.

As you can see, the rendering takes place in JavaScript, in the client. (See xxxx for why). The means that we need a JavaScript templating library for this approach to work. Fortunately there are many to choose from.

API
###

#### Context
filter()


