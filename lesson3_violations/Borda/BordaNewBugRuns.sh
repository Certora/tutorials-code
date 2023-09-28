echo Runing the specs...

certoraRun Borda.sol --verify Borda:BordaMissingRule.spec --msg 'Missing rule also pass in the original'

certoraRun BordaNewBug.sol --verify BordaNewBug:Borda.spec --msg 'Original rules passes in the buggy file'

certoraRun BordaNewBug.sol --verify BordaNewBug:BordaMissingRule.spec --msg 'New rule catches the bug'
