Worklog:
    
06/12/24
    Mission 32
        - SWAN timestep changed to 60s
        - Coupling timestep changed to 60s
        - Added ROLLER_SVENDSEN to dunex.h
            - Can only have one roller code active?
            - Or there's a bug with both
        - Changed cores to 10-WAV 30-OCN
            - NtileI == 5 NtileJ == 6
06/13/24
    Looking into output filesize. 
        - 3D files are big
        - Compression/Deflation seems to save a huge amount of space which makes sense, also possible changing shuffle could help with this?
        - NC_DLEVEL = 4 seems like the best (in agreement with some people online)
    Wrote scripts/compress_netcdf.py and scripts/profile_compression.py
    Trying to get an idea of what changing the parameters does to the results
    Set up git

7/10/24
    Fix forcing etc. for mission32 for comparision

7/11/24
    Looking into QB/breaker formulation
    =====================================
    SWAN using BREAKING CONSTANT 1.0 0.6
               | -> CONstant [alpha] [gamma]
    BREaking  <
               |    BKD [alpha] [gamma0] [a1] [a2] [a3]

    CONSTANT	indicates that a constant breaker index is to be used.	 
    [alpha]	proportionality coefficient of the rate of dissipation.	 
 	    Default: [alpha] = 1.0.	 
    [gamma]	the breaker index, i.e. the ratio of maximum individual	 
 	        wave height over depth.	 
 	    Default: [gamma] = 0.73

    ```fortran
    !
    !     --- calculate fraction of breakers
    !
        IF ( ETOT .GT. 0. ) THEN
    !
    !       --- calculate Qb when Battjes/Janssen breaking is activated
    !
            IF ( ISURF.NE.4                                                   41.38
        &                  ) THEN
            CALL FRABRE (HM, ETOT, QB(KCGRD(1)), KTETA)                    41.47
    !
    !       --- calculate Qb when Thornton/Guza breaking is activated         41.03
    !
            ELSEIF (ISURF.EQ.4) THEN
            WH = (2.*SQRT(2.*ETOT)/HM)**PSURF(5)
            WH = MIN(1.,WH)
            QB(KCGRD(1)) = WH
            ENDIF
    !
        ENDIF
    !
      QB_LOC = QB(KCGRD(1))
    !
    ```

    BREAKING CONSTANT [alpha] [gamma] corresponds to  Battjes&Janssen (`78): ALPHA    0.1000E+01 GAMMA   0.6000E+00

    ```fortran
        !
    !****************************************************************
    !
        SUBROUTINE FRABRE ( HM, ETOT, QBLOC, KTETA )                        41.47 30.77
    !
    !****************************************************************
    !
        USE SWCOMM4                                                         40.41
        USE OCPCOMM4                                                        40.41
    !
        IMPLICIT NONE
    !
    !
    !   --|-----------------------------------------------------------|--
    !     | Delft University of Technology                            |
    !     | Faculty of Civil Engineering                              |
    !     | Environmental Fluid Mechanics Section                     |
    !     | P.O. Box 5048, 2600 GA  Delft, The Netherlands            |
    !     |                                                           |
    !     | Programmers: The SWAN team                                |
    !   --|-----------------------------------------------------------|--
    !
    !
    !     SWAN (Simulating WAves Nearshore); a third generation wave model
    !     Copyright (C) 1993-2019  Delft University of Technology
    !
    !     This program is free software; you can redistribute it and/or
    !     modify it under the terms of the GNU General Public License as
    !     published by the Free Software Foundation; either version 2 of
    !     the License, or (at your option) any later version.
    !
    !     This program is distributed in the hope that it will be useful,
    !     but WITHOUT ANY WARRANTY; without even the implied warranty of
    !     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    !     GNU General Public License for more details.
    !
    !     A copy of the GNU General Public License is available at
    !     http://www.gnu.org/copyleft/gpl.html#SEC3
    !     or by writing to the Free Software Foundation, Inc.,
    !     59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
    !
    !
    !  0. Authors
    !
    !     30.77: Annette Kieftenburg
    !     40.41: Marcel Zijlema
    !     41.47: James Salmon
    !
    !  1. Updates
    !
    !     30.77, Sep. 98: the discontinuity at B = 0.9 has been removed and
    !                     the discontinuity at B = 0.3 is changed in a discontinuity
    !                     at B = 0.2 for which QBLOC = 1.E-9
    !     40.41, Oct. 04: common blocks replaced by modules, include files removed
    !     41.47, Oct. 13: include effect wave directionality
    !
    !  2. Purpose
    !
    !     to compute the fraction of breaking waves in point ix,iy
    !     of the computational grid
    !
    !  3. Method (updated...)
    !
    !      The fraction of breaking waves in a point ix,iy is given by
    !      the implicit relation:
    !
    !        1 - Qb        ETOT
    !        ------ = -8 * -----
    !        ln Qb         HM**2
    !
    !        from which Qb can be found by solving the equation:
    !
    !                         ETOT
    !        F = 1 - Qb + 8 * ----  * ln(Qb) = 0.
    !                           2
    !                         HM
    !
    !        The following appproximation is applied:
    !
    !                            2
    !  (1)|   B = sqrt( 8 ETOT/HM ), i.e. B = Hrms/HM
    !
    !
    !     |   Qo = 0.                                      B <= 0.5
    !  (2)|                 2
    !     |   Qo = ( 2B -1 )                         0.5 < B <= 1
    !
    !
    !     applying the Newton-Raphson procedure (for 0.2<B<1.0):
    !
    !     |   Qb = 0.                                      B <= 0.2
    !     |
    !     |                                   2
    !     |               2  Qo - exp((Qo-1)/B )
    !  (3)|   Qb = Qo  - B   ------------------      0.2 < B <  1.0
    !     |                   2               2
    !     |                  B  - exp((Qo-1)/B )
    !     |
    !     |
    !     |   Qb = 1.                                      B >= 1.0
    !     |
    !
    !     Here the parameters ETOT and HM are determined in the subroutine
    !     SINTGRL
    !
    !  4. Argument variables
    !
    !     ETOT    input  total energy per spatioal gridpoint
    !     HM      input  maximum wave height
    !     KTETA   input  number of directional partitions
    !     QBLOC   output second iteration of the fraction of breaking waves
    !
        REAL    ETOT,  HM,  KTETA, QBLOC
    !
    !  5. Parameter variables
    !
    !  6. Local variables
    !
    !     B       dummy variable
    !     B2      dummy variable: B**2
    !     IENT    number of entries
    !     QO      first estimate of the fraction of breaking waves
    !     Z       dummy variable
    !
        INTEGER IENT
        REAL    B,  B2,  QO,  Z
    !
    !  7. Common blocks used
    !
    !
    !  8. Subroutines used
    !
    !  9. Subroutines calling
    !
    !     SINTGRL
    !
    ! 10. Error messages
    !
    ! 11. Remarks
    !
    ! 12. Structure
    !
    !   ------------------------------------------------------------
    !   Read the total wave energy ETOT and the maximum waveheight HM
    !     If HM > 0. and ETOT > 0., then
    !       Compute factor B according to equation (1)
    !     Else
    !       B = 0
    !     ------------------------------------------------------------
    !     Compute first estimate Qo according to equation (2)
    !     Compute Qb according to equation (3)
    !   ------------------------------------------------------------
    !   End of FRABRE
    !   ------------------------------------------------------------
    !
    ! 13. Source text
    !
        SAVE IENT
        DATA IENT/0/
        IF (LTRACE) CALL STRACE (IENT,'FRABRE')
    !
        IF ( (HM .GT. 0.) .AND. (ETOT .GE. 0.) ) THEN
            B = SQRT(8. * ETOT / (HM*HM) )
            B = B / SQRT(KTETA)
        ELSE
            B = 0.0
        END IF
    !
        IF ( B .LE. 0.5 ) THEN
            QO = 0.
        ELSE IF ( B .LE. 1.0 ) THEN
            QO = (2.*B - 1.)**2
        END IF
    !
        IF ( B .LE. 0.2 ) THEN
            QBLOC = 0.0
        ELSE IF ( B .LT. 1.0 ) THEN
    !
    !       *** second iteration to find Qb ***
    !
            B2 = B*B
            Z  = EXP((QO-1.)/B2)
            QBLOC = QO - B2 * (QO-Z)/(B2-Z)
        ELSE
            QBLOC = 1.0
        END IF
    !
        IF ( TESTFL .AND. ITEST .GE. 110 ) THEN
            WRITE (PRINTF,6120) ETOT, HM, B, QBLOC
    6120   FORMAT (' FRABRE: ETOT  HM  B  QB     : ',4E12.4)
        END IF
    !
    !     End of subroutine FRABRE
        RETURN
        END
    ```

    =====================================
    I can't see why ROLLER_SVENDSEN has to control WAVE_BREAK output other than a bunch of places where it, seems like it's just output from SWAN, but witha bunch of stuff 
    =====================================
    ROMS
    OCEAN.in
    WEC_ALPHA == 0.5d0                        ! 0: all wave dissip goes to break and none to roller.
                                              ! 1: all wave dissip goes to roller and none to breaking.
    http://140.112.69.65/research/coawst/COAWST_TUTORIAL/training_15aug2016/presentations/wednesday/WEC_VF_NK.pdf
    =====================================
