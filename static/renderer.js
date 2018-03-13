var Frontark = {};
var apiUrl = "127.0.0.1/api"

$(document).ready(function(){
    $("#query").submit(function(event){
      query = $("#query > input").val()
      Frontark.searchMovies(query)
      event.preventDefault();
    })
    $("#arca").click(function(){
      Frontark.showArca()
    })

    $("button#toogle-ark").click(function(){
      alert("aaaaa")
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

      var htmlMoviePreview = `
      <div class="col-8 movie-preview">
        <img class="poster-img col-4" src="static/` + movie.posterimg + `" alt="no poster">
        <div class="movie-info col-8">
          <h4 class="title">` + movie.title + `</h4>

          <button id="toogle-ark" class="btn btn-outline-info btn-sm" data-id="`+ movie.themoviedb_id + `">Adicionar</button>

          <p class="overview">` + movie.in_arca + movie.overview + `</p>
          <div class="links">
            <a class="btn btn-outline-dark btn-sm disabled" href="#">IMDB</a> <a class="btn btn-outline-dark btn-sm" href="https://www.themoviedb.org/movie/`+movie.themoviedb_id+`">The Movie Database</a>

          </div>
        </div>
      </div> `
      $movieList.append(htmlMoviePreview)
      console.log("rolou a apendada")

})


}
