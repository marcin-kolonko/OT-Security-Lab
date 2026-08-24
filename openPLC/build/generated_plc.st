PROGRAM program0
  VAR
    RS0 : RS;
    RS1 : BOOL := true;
    RS2 : BOOL := true;
    RS3 : BOOL := false;
  END_VAR

  RS0(S := RS1, R1 := RS3);
  RS2 := RS0.Q1;
END_PROGRAM


CONFIGURATION Config0

  RESOURCE Res0 ON PLC
    TASK task0(INTERVAL := T#20ms,PRIORITY := 0);
    PROGRAM instance0 WITH task0 : program0;
  END_RESOURCE
END_CONFIGURATION
