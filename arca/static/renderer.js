var Frontark = {};
var apiUrl = "127.0.0.1/api"

$(document).ready(function(){
    $("#query").submit(function(event){
      query = $("#query > input").val()
      Frontark.searchMovies(query)
      event.preventDefault();
    })
    $(document).on("click",".toogle-ark",function(){
        var $button_object = $(this)

        let movie_id = $(this).attr("data-id")
        Frontark.ToogleArk(movie_id, $button_object)
        console.log($button_object)
    })

})


Frontark.showArca = function(){
  let url = "api/arca"
  $.get(url,function(data){
    Frontark.renderResults(data);
  })
}

Frontark.searchMovies = function(query){
  let url = "api/search"
  $.get(url, {query: query}, function(data){
    Frontark.renderResults(data);
    console.log("rolou a pesquisa")
  })
}



Frontark.renderResults = function(results){

   $("#movie-list").empty()
   var $movieList = $("#movie-list")

    results.forEach( function(movie){
      var button_status = ""
      var button_false = `<button class="toogle-ark btn btn-outline-info btn-sm " data-toogle="false" data-id="`+ movie.themoviedb_id + `">Adicionar</button>`
      var button_true = `<button class="toogle-ark btn btn-outline-info btn-sm " data-toogle="true" data-id="`+ movie.themoviedb_id + `">Remover</button>`

      if (movie.in_arca == true){
          button_status = button_true
      } else if(movie.in_arca == false){
          button_status = button_false
      } else {
          button_status = `<button class="btn btn-outline-warning btn-sm deactivated">Nada</button>`
      }
      var htmlMoviePreview = `
      <div class="col-8 movie-preview">
        <img class="poster-img col-4" src="static/` + movie.posterimg + `" alt="no poster">
        <div class="movie-info col-8">
          <h4 class="title">` + movie.title + `</h4> ` + button_status + `




          <p class="overview">` + movie.in_arca + movie.overview + `</p>
          <div class="links">
            <a class="btn btn-outline-dark btn-sm disabled" href="#">IMDB</a> <a class="btn btn-outline-dark btn-sm" href="https://www.themoviedb.org/movie/`+movie.themoviedb_id+`">The Movie Database</a>

          </div>
        </div>
      </div> `
      $movieList.append(htmlMoviePreview)



})

}

Frontark.ToogleArk = function(movie_id, button_object){
 // alert(movie_id)

    let url = "/api/arca/" +  movie_id
    var $button = button_object
    console.log($button.attr("data-toogle"))
    if ($button.attr("data-toogle") == "false"){
    let request = $.post(url, function(){$button.html("Remover"); $button.attr("data-toogle","true")})
    .fail(function(){alert("nao deu")})
    }
    else if ($button.attr("data-toogle") == "true") {
        let request = $.ajax({
            url: url,
            method: "DELETE",
            success: function(){$button.html("Adicionar"); $button.attr("data-toogle","false")} })

            .fail(function(){alert("nao deu")})
        }


        }
