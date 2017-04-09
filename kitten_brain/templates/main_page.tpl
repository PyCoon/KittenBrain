<!DOCTYPE html>


<html lang="fr">
    <head>

       <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
        <title>Piece Of brain</title>
        <meta name="description" content="Piece Of Brain">
        <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="//code.jquery.com/ui/1.11.4/themes/smoothness/jquery-ui.css">

  <script src="//code.jquery.com/jquery-1.10.2.js"></script>
  <script src="//code.jquery.com/ui/1.11.4/jquery-ui.js"></script>
 <style>
    fieldset {
      border: 0;
    }
    select{

width: 398px;

    border-bottom-right-radius: 4px;


    border-bottom-left-radius: 4px;

    border-top-right-radius: 4px;

    border-top-left-radius: 4px;

    border: 1px solid #d3d3d3;
    font-weight: normal;
    color: #555555;


    font-family: Verdana,Arial,sans-serif;
    font-size: 1.1em;


    display: inline-block;
    overflow: hidden;
    position: relative;
    text-decoration: none;
    cursor: pointer;
     }

    label {
      display: block;
      margin: 30px 0 0 0;
    }
    .overflow {
      height: 200px;
    }

    select {
    width: 200px;
    }


#wrap {
   width:100%;
   margin:0 auto;
}
#left_col {
   float:left;
   width:30%;
}
#right_col {
   float:right;
   width:70%;
}
.content_boxe{
border-style: outset;
   width:85%;
}
.content_date{
font-style: italic;
fon-color: grey;
}
.for_del:hover {
 background-color: yellow;
}
.content_description{
font-style: italic;
}
.content_content{

}
  </style>
    </head>

    <body>
<div id="wrap">
<h1>Kitten Brain</h1>
    <div id="left_col">
    <fieldset id="search_box">
        <label>Category</label>
<select id="category_selector">
      <!--Category here -->
</select>

<label>Sub-category</label>
<select id="sub_category_selector">
      <!--Non implémenté.
<input name="date_recherche" />
       -->
</select></br>

<label for="to_search_description">Description:</label>
<input id="to_search_description" value="" placeholder="Description"></br>

        <button id="search_button">Rechercher</button>
        </fieldset>


<fieldset id="insert_box">
<label for="insert_category">Categorie:</label>
    <input id="insert_category" type="text" ></br>
    <label for="insert_sub_category">Sous-catégorie:</label>
    <input id="insert_sub_category" type="text" ></br>
    <label for="insert_description">Description:</label>
    <input id="insert_description" type="text" ></br>
    <label for="insert_content">Contenu:</label>
    <textarea id="insert_content" type="text" ></textarea></br>
  <span id="alert_box_insert_box"></span></br>
     <button id="add_category_button">Inserer</button>



</fieldset>
</div>
    <div id="right_col">

<article>


</article>
</div>
    </div>

<script type="text/javascript" src="/static/base_search.js"></script>
    </body>
</html>