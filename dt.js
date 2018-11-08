var readlineSync = require('readline-sync')
var util = require('util')
function rand() {
   return Math.floor(Math.random() * Math.floor(32767));
}

function shuffle_list (list, len)
{
    //We'll just be swapping 100 times. Could be more/less. Doesn't matter much.
    var n = Math.trunc (100);
    var a = Math.trunc (0);
    var b = Math.trunc (0);
    var buf = Math.trunc (0);
    //Random enough for common day use..
    while(n--)
    {
        //Get random locations and swap
        a = Math.trunc (rand () % len);
        b = Math.trunc (rand () % len);
        buf = Math.trunc (list[a]);
        list[a] = Math.trunc (list[b]);
        list[b] = Math.trunc (buf);
    }

    // "shuffled to ordered state" fix:
    if(check_array (list, len))
    shuffle_list (list, len);
}

function do_flip (list, length, num)
{
    //Flip a part on an array
    var swap;
    var i = Math.trunc (0);
    for(i; i <-- num; i++)
    {
        swap = Math.trunc (list[i]);
        list[i] = Math.trunc (list[num]);
        list[num] = Math.trunc (swap);
    }

}

function check_array (arr, len)
{
    while(-- len)
    {
        if(arr[len] != (arr[len - 1] + 1))
        return Math.trunc (0);
    }

    return Math.trunc (1);
}

function number_reversal_game ()
{
    process.stdout.write(util.format("Number Reversal Game. Type a number to flip the first n numbers."));
    process.stdout.write(util.format("Win by sorting the numbers in ascending order.\n"));
    process.stdout.write(util.format("Anything besides numbers are ignored.\n"));
    process.stdout.write(util.format("\t  |1__2__3__4__5__6__7__8__9|\n"));
    var list =[1, 2, 3, 4, 5, 6, 7, 8, 9];
    shuffle_list (list, 9);
    var tries = Math.trunc (0);
    var i;
    var input;
    while(! check_array (list, 9))
    {
        ((tries < 10) ? process.stdout.write(util.format("Round %d :  ", tries)): process.stdout.write(util.format("Round %d : ", tries)));
        for(i = Math.trunc (0); i < 9; i++)
        process.stdout.write(util.format("%d  ", list[i]));
        process.stdout.write(util.format("  Gimme that number:"));
        while(1)
        {
            //Just keep asking for proper input
            input = Number(readlineSync.question(''));
            if(input > 1 && input < 10)
            break;
            process.stdout.write(util.format("\n%d - Please enter a number between 2 and 9:", input));
        }

        tries++;
        do_flip (list, 9, input);
    }

    process.stdout.write(util.format("Hurray! You solved it in %d moves!\n", tries));
}

function main ()
{
    number_reversal_game ();
    return Math.trunc (0);
}

main();