var Frontark = {};
var apiUrl = "127.0.0.1/api"

$(document).ready(function() {
    $("body").niceScroll();

    $("#query").submit(function(event) {
        query = $("#query > input").val()

        event.preventDefault();
        Frontark.cleanMain();

        Frontark.searchMovies(query)



    })

    $(document).on("click", ".toogle-ark", function() {
        var $button_object = $(this)

        let movie_id = $(this).attr("data-id")
        Frontark.ToogleArk(movie_id, $button_object)
        console.log($button_object)
    })

    $(document).on("click", "#search-more", function() {
        query = $("#query > input").val()
        Frontark.searchMoreMovies(query)

    })

})



$(document).ajaxStart(function() {
    $("body").addClass("loading");



});

$(document).ajaxStop(function() {

    $("body").removeClass("loading");



});






Frontark.showArca = function() {
    let url = "api/arca"
    $.get(url, function(data) {
        Frontark.renderResults(data);
    })
}

Frontark.showList = function(username) {
    let url = "api/arca"
    $.get(url, {
        user: username
    }, function(data) {
        Frontark.renderResults(data);
    })
}

Frontark.showPeople = function() {
    let url = "api/users"

    $.get(url, function(data) {
        Frontark.renderPeople(data);
    })
}

Frontark.searchMovies = function(query) {
    let url = "api/search"
    $.get(url, {
        query: query
    }, function(data) {
        Frontark.renderResults(data);
        button = `<button id="search-more" >Buscar Mais</button>`
        $("#movie-list").append(button)
        console.log("rolou a pesquisa")
    })
}

Frontark.searchMoreMovies = function(query) {
    let url = "api/search"
    $.get(url, {
        query: query,
        more: true
    }, function(data) {
        Frontark.renderResults(data);

        console.log("rolou a pesquisa")
    })
}

Frontark.renderPeople = function(results) {
    $("#people-list").empty()
    var $peopleList = $("#people-list")
    results.forEach(function(person) {
        var html = ` <div class="person">` + person.login + `</div>`
        $peopleList.append(html)
    })
};

Frontark.cleanMain = function() {
    $("main").html(`<div id="movie-list"> </div>`)
};

Frontark.renderResults = function(results) {

    $("#movie-list").empty()
    var $movieList = $("#movie-list")


    results.forEach(function(movie, index) {

        index = index + 1
        var load_more = ''
        var group = Math.ceil(index / 16)
        var visibility = ` hidden`

        if (group == 1) {
            visibility = ``

        }

        if (index % 16 == 0) {
            load_more = `<div class="load-more ` + (group) + visibility + ` " data-group="`+ (group+1)+`">Carregar Mais</div>`

        }


        var button_status = ""
        var button_false = `<button class="toogle-ark" data-toogle="false" data-id="` + movie.id_ + `">Adicionar</button>`
        var button_true = `<button class="toogle-ark" data-toogle="true" data-id="` + movie.id_ + `">Remover</button>`
        var status_container = ""
        if (movie.in_arca == true) {
            button_status = button_true
            status_container = "saved"

        } else if (movie.in_arca == false) {
            button_status = button_false
            status_container = ""
        } else {
            button_status = `<button class="">Nada</button>`
        }

        var htmlMoviePreview = `
      <div class="movie-preview ` + group + visibility + `">
        <div class="img-container ` + status_container + `">
        <img class="status-icon" src="../static/images/success.png">
        <img class="poster-img" scr="" data-src="../static/posters/` + movie.poster_path + `" alt="Não encontramos um poster para esse filme" style="text-align:center"><div class="img-overlay"> ` + button_status + `</div></div>
        <div class="movie-info">
          <div class="head">


          <h4 class="title">` + movie.title + `</h4>
          <span class="date">` + movie.release_date + `  </span>
          </div>



          <p class="overview">` + movie.overview + `</p>
          <div class="links">
            <h5>Links:</h5><a class="" href="#">IMDB</a> <a class="" href="https://www.themoviedb.org/movie/` + movie.id_ + `">The Movie Database</a>

          </div>
        </div>
      </div>
      ` + load_more
        $movieList.append(htmlMoviePreview)


    })


$(".overview").niceScroll({
    cursorwidth: 3,
    cursorfixedheight: 20
});

$("body").getNiceScroll().resize()


$(".poster-img:visible").Lazy({
    afterLoad: function(element) {
            console.log("cabou")
    }
});

var hand = function(direction) {
    var $element = $(this.element)
    var groupId = $element.attr("data-group")

    console.log(groupId)

    $(`div.load-more.`+(groupId-1)).addClass("passed")
    $(`div.load-more.`+(groupId-1)).html("")
    $(`.movie-preview.`+groupId).removeClass("hidden")
    $(`div.load-more.`+groupId).removeClass("hidden")


    $(".poster-img:visible").Lazy();

    $(".overview").niceScroll({
        cursorwidth: 3,
        cursorfixedheight: 20
    });

    $("body").getNiceScroll().resize()
    setTimeout(function(){
        $(`div.load-more.`+groupId).waypoint({
            handler:hand,
            offset: "bottom-in-view"
        })
    },2000)

}

$("div.load-more.1").waypoint({
        handler: hand,
        offset: "bottom-in-view"
    })

}

Frontark.ToogleArk = function(movie_id, button_object) {
    // alert(movie_id)

    let url = "/api/arca/" + movie_id
    var $button = button_object
    var $container = $button.parents(".img-container")
    var name = $("#user-name").html()
    console.log($button.attr("data-toogle"))
    if ($button.attr("data-toogle") == "false") {
        let request = $.post(url, {
                user: name
            }, function() {
                $button.html("Remover"), $container.addClass("saved"), $button.attr("data-toogle", "true")
            })
            .fail(function() {
                alert("nao deu")
            })
    } else if ($button.attr("data-toogle") == "true") {
        let request = $.ajax({
                url: url,
                data: {
                    user: name
                },
                method: "DELETE",
                success: function() {
                    $button.html("Adicionar");
                    $container.removeClass("saved"), $button.attr("data-toogle", "false")
                }
            })

            .fail(function() {
                alert("nao deu")
            })
    }


}
