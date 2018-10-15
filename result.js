var readlineSync = require('readline-sync')
var util = require('util')
/* ({Test}) */
function main ()
{
    for(i = 0; i < 10; console.log(util.format("%d", i)))
    {
        i++;
    }

    console.log(util.format("Hello World!"));
    console.log(util.format("Hello" + "HaroHappi" + "Poppin'Party"));
    var alet = 1;
    var r = 2.2;
    var r2 = 2.;
    console.log(util.format("This is a floating point number: %d", 2.23));
    /*
    __++ ** --&$
    This a multiline comment asdasdsadasdasdasdasdasdsa
    sadsadasdasdsad
    sadasdasdsadsa
    int i = 1;
    */
    //Wow) it's a first comment!
    //This is the second comment.
    if(((1 + 1) + 1 - 1) == 2)
    //Another comment {
    {
        //This is a comment and this is another
        //
        /**/
        /*@@@@@how about;
    //srts
    this? */
        var i = 2;
        i = Number(readlineSync.question(''));
        var i = ';';
    }

    for(i = (0 + 1); i < 5; i++)
    {
        console.log(util.format("%d %d %d", i, i, i));
        console.log(util.format("This \" is; an arbitrarily; long string; *designed to test* the string joiner %d. %s ", i, "Whoaaa. is this another string???"));
        console.log(util.format("Hmmmm \" I escaped \
    some string here %s", '\''));
    }

    for(console.log(util.format("%d" + "%d\n", i, i)); i < 10; console.log(util.format("%d\n", i)))
    {
        i++;
    }

    var t, v, x;
    for(t = Number(readlineSync.question('')); i < 10; x = Number(readlineSync.question('')))
    {
        i++;
    }

    var test = "Hello; World!";
    // if (2 == 2) printf("Benerrrr");
    // while (2 == 2) printf("Benerrrr loopnyo");
    do
    {
        i++;
    }

    while(i < 5);
    var c = 0;
    var b = {ptr : c};
    b.ptr = 10;
    var d = b.ptr * c.ptr;
    console.log(util.format("%d" + "%d\n", b.ptr, d.ptr));
    console.log(util.format("%d %d %s\n" + "%d", b.ptr, d.ptr));
    console.log(util.format("((abcd"));
    console.log(util.format("(abcd"));
    console.log(util.format("abcd"));
    b.ptr = Number(readlineSync.question(''));
    d = Number(readlineSync.question(''));
    return 0;
}

function mantap ()
{
    console.log(util.format("Halloooooooo"));
}

function cetak (a)
{
    console.log(util.format("%d", a.ptr));
}

main();