import unittest

from mistools import misflatfile
#from mistools import misflatfile


## currently theses tests really just ensure nothing has gone backwards
## as we add elements, eventually actual data spot checks, fill
## checks possibly error reporting checks should be integrated

TEST_FIXTURE_PATH_TEMPLATE = "../tmp/%s" # cwd is package root
TEST_FIXTURE_PATH = "../tmp/"

class Test_Mis_FF_Parser(unittest.TestCase):

    def test_parse_cb(self):

        ff_path = TEST_FIXTURE_PATH_TEMPLATE % "U22218CB.DAT"

        data = misflatfile.cb_mis_parse(ff_path)

        self.assertEqual( len(data), 1116 )

        data = misflatfile.cb_mis_parse(ff_path, headers = True)

        self.assertEqual( len(data), 1117 )

    def test_parse_sb(self):

        ff_path = TEST_FIXTURE_PATH_TEMPLATE % "U22218SB.DAT"

        data = misflatfile.sb_mis_parse(ff_path)

        self.assertEqual( len(data), 4251 )

        data = misflatfile.sb_mis_parse(ff_path, headers = True)

        self.assertEqual( len(data), 4252 )

    def test_parse_xb(self):

        ff_path = TEST_FIXTURE_PATH_TEMPLATE % "U22218XB.DAT"

        data = misflatfile.xb_mis_parse(ff_path)

        self.assertEqual( len(data['XB']), 286)
        self.assertEqual( len(data['XF']), 400)
        self.assertEqual( len(data['XE']), 432)

        data = misflatfile.xb_mis_parse(ff_path, headers = True)

        self.assertEqual( len(data['XB']), 287)
        self.assertEqual( len(data['XF']), 401)
        self.assertEqual( len(data['XE']), 433)

    def test_parse_xb_bulk(self):

        ff_paths = [

            TEST_FIXTURE_PATH_TEMPLATE % "U22216XB.DAT",
            TEST_FIXTURE_PATH_TEMPLATE % "U22218XB.DAT"
        ]


        data = misflatfile.xb_mis_parse(ff_paths)

        self.assertEqual( len(data['XB']), 416 )
        self.assertEqual( len(data['XF']), 585 )
        self.assertEqual( len(data['XE']), 625 )

        data = misflatfile.xb_mis_parse(ff_paths, headers = True)

        self.assertEqual( len(data['XB']), 417 )
        self.assertEqual( len(data['XF']), 586 )
        self.assertEqual( len(data['XE']), 626 )

    def test_parse_sx(self):

        ff_path = TEST_FIXTURE_PATH_TEMPLATE % "U22218SX.DAT"

        data = misflatfile.sx_mis_parse(ff_path)

        self.assertEqual( len(data), 4589 )

        data = misflatfile.sx_mis_parse(ff_path, headers = True)

        self.assertEqual( len(data), 4590 )

    def test_parse_sd(self):

        ff_path = TEST_FIXTURE_PATH_TEMPLATE % "U22218SD.DAT"

        data = misflatfile.sd_mis_parse(ff_path)

        self.assertEqual( len(data), 108 )

        data = misflatfile.sb_mis_parse(ff_path, headers = True)

        self.assertEqual( len(data), 109 )

    def test_parse_sc(self):

        ff_path = TEST_FIXTURE_PATH_TEMPLATE % "U22216SC.DAT"

        data = misflatfile.sc_mis_parse(ff_path)

        self.assertEqual( len(data), 4 )

        data = misflatfile.sc_mis_parse(ff_path, headers = True)

        self.assertEqual( len(data), 5 )

    def test_parse_sy(self):

        ff_path = TEST_FIXTURE_PATH_TEMPLATE % "U22218SY.DAT"

        data = misflatfile.sy_mis_parse(ff_path)

        self.assertEqual( len(data), 16 )

        data = misflatfile.sy_mis_parse(ff_path, headers = True)

        self.assertEqual( len(data), 17 )

    def test_parse_ss(self):

        ff_path = TEST_FIXTURE_PATH_TEMPLATE % "U22216SS.DAT"

        data = misflatfile.ss_mis_parse(ff_path)

        self.assertEqual( len(data), 2548 )

        data = misflatfile.ss_mis_parse(ff_path, headers = True)

        self.assertEqual( len(data), 2549 )

    def test_parse_sv(self):

        ff_path = TEST_FIXTURE_PATH_TEMPLATE % "U22222SV.DAT"

        data = misflatfile.sv_mis_parse(ff_path)

        self.assertEqual( len(data), 158 )

        data = misflatfile.sv_mis_parse(ff_path, headers = True)

        self.assertEqual( len(data), 159 )

    def test_parse_se(self):

        ff_path = TEST_FIXTURE_PATH_TEMPLATE % "U22214SE.DAT"

        data = misflatfile.se_mis_parse(ff_path)

        self.assertEqual( len(data), 71 )

        data = misflatfile.se_mis_parse(ff_path, headers = True)

        self.assertEqual( len(data), 72 )

    def test_parse_se(self):

        ff_path = TEST_FIXTURE_PATH_TEMPLATE % "U22222EB.DAT"

        data = misflatfile.eb_mis_parse(ff_path)

        self.assertEqual( len(data), 157 )

        data = misflatfile.eb_mis_parse(ff_path, headers = True)

        self.assertEqual( len(data), 158 )


    # ANNUAL
    def test_parse_sp(self):

        ff_path = TEST_FIXTURE_PATH_TEMPLATE % "U22210SP.DAT"

        data = misflatfile.sp_mis_parse(ff_path)

        self.assertEqual( len(data), 210 )

        data = misflatfile.sp_mis_parse(ff_path, headers = True)

        self.assertEqual( len(data), 211 )

    def test_parse_sp_bulk(self):

        ff_paths = [

            TEST_FIXTURE_PATH_TEMPLATE % "U22210SP.DAT",
            TEST_FIXTURE_PATH_TEMPLATE % "U22210SP.DAT"
        ]

        data = misflatfile.sp_mis_parse(ff_paths)

        self.assertEqual( len(data), 420 )

        data = misflatfile.sp_mis_parse(ff_paths, headers = True)

        self.assertEqual( len(data), 421 )

    def test_parse_sf(self):

        ff_path = TEST_FIXTURE_PATH_TEMPLATE % "U22210SF.DAT"

        data = misflatfile.sf_mis_parse(ff_path)

        self.assertEqual( len(data), 2335 )

        data = misflatfile.sf_mis_parse(ff_path, headers = True)

        self.assertEqual( len(data), 2336 )

    def test_parse_fa(self):

        ff_path = TEST_FIXTURE_PATH_TEMPLATE % "U22210FA.DAT"

        data = misflatfile.fa_mis_parse(ff_path)

        self.assertEqual( len(data), 6681 )

        data = misflatfile.fa_mis_parse(ff_path, headers = True)

        self.assertEqual( len(data), 6682 )

class Test_Mis_Export(unittest.TestCase):

    def test_export_sx(self):

        misflatfile.sx_mis_export('222', TEST_FIXTURE_PATH)
        self.assertEqual(1,1)

    def test_export_sy(self):

        misflatfile.sy_mis_export('222', TEST_FIXTURE_PATH)
        self.assertEqual(1,1)

    def test_export_ss(self):

        misflatfile.ss_mis_export('222', TEST_FIXTURE_PATH)
        self.assertEqual(1,1)

    def test_export_sd(self):

        misflatfile.sd_mis_export('222', TEST_FIXTURE_PATH)
        self.assertEqual(1,1)

    def test_export_sc(self):

        misflatfile.sc_mis_export('222', TEST_FIXTURE_PATH)
        self.assertEqual(1,1)

    def test_export_xb(self):

        misflatfile.xb_mis_export('222', TEST_FIXTURE_PATH)
        self.assertEqual(1,1)

    def test_export_sb(self):

        misflatfile.sb_mis_export('222', TEST_FIXTURE_PATH)
        self.assertEqual(1,1)

    def test_export_cb(self):

        misflatfile.cb_mis_export('224', TEST_FIXTURE_PATH)
        self.assertEqual(1,1)

    def test_export_sg(self):

        misflatfile.sg_mis_export('222', TEST_FIXTURE_PATH)
        self.assertEqual(1,1)

    def test_export_sv(self):

        misflatfile.sv_mis_export('222', TEST_FIXTURE_PATH)
        self.assertEqual(1,1)

    def test_export_eb(self):

        misflatfile.eb_mis_export('224', TEST_FIXTURE_PATH)
        self.assertEqual(1,1)


if __name__ == '__main__':
    unittest.main()
