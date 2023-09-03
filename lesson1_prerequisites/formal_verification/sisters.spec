/* Four sisters riddle
 * -------------------
 */

// The months
definition September() returns uint8 = 9;
definition October() returns uint8 = 10;
definition November() returns uint8 = 11;
definition December() returns uint8 = 12;

/** @title Find the sister's birth months
 *  See Birth Months riddle from:
 *  https://www.braingle.com/brainteasers/teaser.php?op=2&id=52499&comm=0
 *
 *  The parameters to the rule are the sisters' birth months.
 */
rule sistersBirthMonths(
    uint8 Sara,
    uint8 Ophelia,
    uint8 Nora,
    uint8 Dawn
) {
    // Each sister was born in one of the four months
    require Sara >= September() && Sara <= December();
    require Ophelia >= September() && Ophelia <= December();
    require Nora >= September() && Nora <= December();
    require Dawn >= September() && Dawn <= December();

    // "None of us have an initial that matches the initial of her birth month."
    require (
        Sara != September() &&
        Ophelia != October() &&
        Nora != November() &&
        Dawn != December()
    );

    // Ophelia is not the girl who was born in September
    require Ophelia != September();

    // Nora is not the girl who was born in September
    require Nora != September();

    // Nora's birth month does not start with a vowel
    require Nora != October();

    // The sisters were born on different months
    require (
        Sara != Ophelia &&
        Sara != Nora &&
        Sara != Dawn &&
        Ophelia != Nora &&
        Ophelia != Dawn &&
        Nora != Dawn
    );

    satisfy true;
}


/// @title Verify that the solution is unique
rule solutionIsUnique(
    uint8 Sara,
    uint8 Ophelia,
    uint8 Nora,
    uint8 Dawn
) {
    // Each sister was born in one of the four months
    require Sara >= September() && Sara <= December();
    require Ophelia >= September() && Ophelia <= December();
    require Nora >= September() && Nora <= December();
    require Dawn >= September() && Dawn <= December();

    // "None of us have an initial that matches the initial of her birth month."
    require (
        Sara != September() &&
        Ophelia != October() &&
        Nora != November() &&
        Dawn != December()
    );

    // Ophelia is not the girl who was born in September
    require Ophelia != September();

    // Nora is not the girl who was born in September
    require Nora != September();

    // Nora's birth month does not start with a vowel
    require Nora != October();

    // The sisters were born on different months
    require (
        Sara != Ophelia &&
        Sara != Nora &&
        Sara != Dawn &&
        Ophelia != Nora &&
        Ophelia != Dawn &&
        Nora != Dawn
    );

    assert (
        Sara == October() &&
        Ophelia == November() &&
        Nora == December() &&
        Dawn == September()
    );
}
