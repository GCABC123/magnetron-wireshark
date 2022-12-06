#
# Wireshark tests
#
# SPDX-License-Identifier: GPL-2.0-or-later
#
'''Follow QUIC/HTTP2 Stream tests'''

import subprocesstest
import fixtures


@fixtures.mark_usefixtures('test_env')
@fixtures.uses_fixtures
class case_follow_multistream(subprocesstest.SubprocessTestCase):
    def test_follow_http2_multistream(self, cmd_tshark, capture_file, features):
        '''Checks whether Follow HTTP2 correctly handles multiple streams on the same packet.'''
        # If we don't have nghttp2, we output the compressed headers.
        # We could test against the expected output in that case, but
        # just skip for now.
        if not features.have_nghttp2:
            self.skipTest('Requires nghttp2.')
        # Test 1:
        # 1. While following stream 25 we should ignore stream 21 at frame 65
        proc = self.assertRun((cmd_tshark,
                                '-r', capture_file('http2_follow_multistream.pcapng'),
                                '-qz', 'follow,http2,raw,0,25',
                                ))

        self.assertIn("""\
===================================================================
Follow: http2,raw
Filter: tcp.stream eq 0 and http2.streamid eq 25
Node 0: 10.9.0.2:59246
Node 1: 104.16.40.2:443
000000073a6d6574686f6400000003474554000000053a70617468000000312f6d656469612f6a732f66697265666f785f666972737472756e2d62756e646c652e3464633733383035353861622e6a730000000a3a617574686f726974790000000f7777772e6d6f7a696c6c612e6f7267000000073a736368656d650000000568747470730000000a757365722d6167656e74000000444d6f7a696c6c612f352e3020285831313b204c696e7578207838365f36343b2072763a35322e3029204765636b6f2f32303130303130312046697265666f782f35322e3000000006616363657074000000032a2f2a0000000f6163636570742d6c616e67756167650000000e656e2d55532c656e3b713d302e350000000f6163636570742d656e636f64696e6700000011677a69702c206465666c6174652c20627200000007726566657265720000003668747470733a2f2f7777772e6d6f7a696c6c612e6f72672f656e2d55532f66697265666f782f35322e302e312f666972737472756e2f
00000408000000001900be0000
	000000073a7374617475730000000332303000000004646174650000001d5765642c203239204d617220323031372031313a35393a333020474d540000000c636f6e74656e742d74797065000000276170706c69636174696f6e2f6a6176617363726970743b20636861727365743d227574662d38220000001b6163636573732d636f6e74726f6c2d616c6c6f772d6f726967696e000000012a0000000d63616368652d636f6e74726f6c000000246d61782d6167653d3331353336303030302c207075626c69632c20696d6d757461626c6500000010636f6e74656e742d656e636f64696e6700000004677a697000000017636f6e74656e742d73656375726974792d706f6c696379000004737363726970742d737263202773656c6627202a2e6d6f7a696c6c612e6e6574202a2e6d6f7a696c6c612e6f7267202a2e6d6f7a696c6c612e636f6d2027756e736166652d696e6c696e65272027756e736166652d6576616c27202a2e6f7074696d697a656c792e636f6d206f7074696d697a656c792e73332e616d617a6f6e6177732e636f6d207777772e676f6f676c657461676d616e616765722e636f6d207777772e676f6f676c652d616e616c79746963732e636f6d207461676d616e616765722e676f6f676c652e636f6d207777772e796f75747562652e636f6d20732e7974696d672e636f6d3b20696d672d737263202773656c6627202a2e6d6f7a696c6c612e6e6574202a2e6d6f7a696c6c612e6f7267202a2e6d6f7a696c6c612e636f6d20646174613a202a2e6f7074696d697a656c792e636f6d207777772e676f6f676c657461676d616e616765722e636f6d207777772e676f6f676c652d616e616c79746963732e636f6d202a2e74696c65732e6d6170626f782e636f6d206170692e6d6170626f782e636f6d206372656174697665636f6d6d6f6e732e6f72672061642e646f75626c65636c69636b2e6e65743b2064656661756c742d737263202773656c6627202a2e6d6f7a696c6c612e6e6574202a2e6d6f7a696c6c612e6f7267202a2e6d6f7a696c6c612e636f6d3b206672616d652d737263202a2e6f7074696d697a656c792e636f6d207777772e676f6f676c657461676d616e616765722e636f6d207777772e676f6f676c652d616e616c79746963732e636f6d207777772e796f75747562652d6e6f636f6f6b69652e636f6d20747261636b6572746573742e6f7267207777772e73757276657967697a6d6f2e636f6d206163636f756e74732e66697265666f782e636f6d206163636f756e74732e66697265666f782e636f6d2e636e207777772e796f75747562652e636f6d3b207374796c652d737263202773656c6627202a2e6d6f7a696c6c612e6e6574202a2e6d6f7a696c6c612e6f7267202a2e6d6f7a696c6c612e636f6d2027756e736166652d696e6c696e65273b20636f6e6e6563742d737263202773656c6627202a2e6d6f7a696c6c612e6e6574202a2e6d6f7a696c6c612e6f7267202a2e6d6f7a696c6c612e636f6d202a2e6f7074696d697a656c792e636f6d207777772e676f6f676c657461676d616e616765722e636f6d207777772e676f6f676c652d616e616c79746963732e636f6d202a2e74696c65732e6d6170626f782e636f6d206170692e6d6170626f782e636f6d3b206368696c642d737263202a2e6f7074696d697a656c792e636f6d207777772e676f6f676c657461676d616e616765722e636f6d207777772e676f6f676c652d616e616c79746963732e636f6d207777772e796f75747562652d6e6f636f6f6b69652e636f6d20747261636b6572746573742e6f7267207777772e73757276657967697a6d6f2e636f6d206163636f756e74732e66697265666f782e636f6d206163636f756e74732e66697265666f782e636f6d2e636e207777772e796f75747562652e636f6d0000000d6c6173742d6d6f6469666965640000001d5468752c203032204d617220323031372031303a33363a333220474d54000000197374726963742d7472616e73706f72742d7365637572697479000000106d61782d6167653d333135333630303000000004766172790000000f4163636570742d456e636f64696e6700000010782d6261636b656e642d7365727665720000002b6434373333376330323631352e626564726f636b2d70726f642e75732d776573742e6d6f7a2e776f726b7300000011782d636c61636b732d6f7665726865616400000013474e552054657272792050726174636865747400000016782d636f6e74656e742d747970652d6f7074696f6e73000000076e6f736e6966660000000f782d6672616d652d6f7074696f6e730000000444454e590000000c782d726f626f74732d746167000000056e6f6f647000000010782d7873732d70726f74656374696f6e0000000d313b206d6f64653d626c6f636b0000000f63662d63616368652d737461747573000000034849540000000673657276657200000010636c6f7564666c6172652d6e67696e780000000663662d72617900000014333437326139643836653930373334332d414d53
	0003f80000000000191f8b08000000000000037c55db6ee336107def5724ecc220615ac906db3ec850b740364153e4d266bb794917062d8d646e255220295f56d6bf77a84b6ca5415f649373869c3967662853ea7625e8f4e44e7f97792ea288542a81542a48085b0bf362a89b79ff37b8de8a9bd48802a2b452b1935a515693cac2897546c68eccbd2370c75574fa9e1b2eb9e59a570738b0da80ab8c3a8167087250995bcdde7f8df0fa33f211025b2df1287ace0f461642c3c5e108c16a880437d13b4a7e4cb76226db9066b156a9cc080b12e104252b6d1d61dc0e30fcaf23db1bad8971bd912ad19b4024c9d51a94bb95d68102434901d68a0c085ff1d37386b1608ae6aa10329f4cce683065bffacfdf81ffd617bc390b1c58478f706c32a13ad2533201bf8cc81454ac13f8f27873a98b522bbc6f84679850450de303d797b9444c702d0da47a7b27be69f304c62203bf441f7eee8e0f0c94b98881124cdec1d6451d1784bf6ca4db452a0d725aa9c5fa82e03d7a1a9189363293eaedb07a5a721d0b4f78d061197711049968a9bac74bf67be269457612e9e55f561e3d998cd7a7a82c9695a872473068f9ffaa8d7d03a76ff506cca5b040d994fcd6492adb732a2abda2070eb0da3c891253b481705845adcc5ce31adc5fb2005d397a54b86abf4fe987f373d6f08b9fda9f7454a83688adc5420299ad1ce63925e51603c572b9cc85b7e45a24be5b1a9e1f3972c56adf0626ea89f499dd8a1d98fdfef92b97510d9ec2d071891219d1ba618dcf91bb77016a062aa1124fe126282bbbc23c1b1e1f2e70fe82be79e1d961ef90c1860cfb1daad06335ca45a6c86d27242a6258d7846dbbbae8f7cf0ff741290cb20c6db46c6e37d2c52bea825817855009ab631461c8382ca963f3a501f1cfbcdd3760e5772061f26a3fd5a6588012cbdc7baddfb2a2e0bdb9786556622d33e1bc297b65b2325355b9282aeb166b3032dd9170f70ad3eecbae861798469983c31097af60b9464e48b8c1eda6e1e588359c62e73ca7bece6783d83ca644abdb6ec501994e463e69cf61d0d54d8f7fec086af1eb11be355f2313573d4d2da6781bf36920ab0565ff05ddbf70d6227623c41098b00f1bf587d12518b7a3a49d500fa5bb5104c756de6f9ce8d2cd90195ee7620979d83b1fc00d1ba8e9d418a8f9dcaeee509aa74e993692e52892deb193e8c0ead39164978362adfbe6a8fe5fdcfdbd18214ea6a11b5a65bc9ea3aef8d84be60ddcb17018b15f9cccf145d08f90e0948d1d35537286b3c24995596ceb79d725b554d285c7e1e3a0daefeb060ba619a6e5b73f2b30bbe149e96f60fcd86bf450c230e03370fd8cff040eb9b5f4385338bcb9810f83d6c7033274a379c98fa6734886b13ff3531a63652fb10ed1cd7ff8170000ffff030036351cd507080000
	000000000100000019
===================================================================
""".replace("\r\n", "\n"),
            proc.stdout_str)


    def test_follow_quic_multistream(self, cmd_tshark, capture_file):
        '''Checks whether Follow QUIC correctly handles multiple streams on the same packet.'''

        # Test 2:
        # 1. While following stream 40 we should ignore stream 36 at frame 426, and stream 11 at frame 623
        proc = self.assertRun((cmd_tshark,
                                '-r', capture_file('quic_follow_multistream.pcapng'),
                                '-qz', 'follow,quic,raw,0,40',
                                ))

        self.assertIn("""\
===================================================================
Follow: quic,raw
Filter: quic.connection.number eq 0 and quic.stream.stream_id eq 40
Node 0: 10.0.2.15:57172
Node 1: 172.217.5.110:443
01143000d1aed782e4a7dd81a3a280a0df9f9e9d9c9b
	010f3700d982fd819380adf89eeab0aeac00424203500200e4d7dcfefe2fa7a5df3632669896a543445e8a68d10ebc13d704f6af5e7460740ba4e67985c9c8c6b3b9b6b65ce9af3404e6213f749da27b3c523060867c215f30e43343a1a055e4924757cba0cd8fb3b9219712521b197ba3b55d06907660c4a29fee6cb94abce7d1800346c603f68021dad3fdfb7bbada302be0f3e9456a7134b3f0f9c82deb126fa10875b570f96976ea311b77d2e620d2a3cd652555db30dc8da347a1f2be10bc129a180d576cb394a9cfef499a0a037f3a34c6e3047507f07fff215080120182587a6277871ae3e16e2c44ecebdbe77ce1ca6f447a35d2c89749a5054e09679b28fa46bbc58dd10b404ac36436c3e2305f72ff18b847b85e181c0f0ba058c05780a2a12f8ccac69fdf819e4e60b2765852c6304c44064b9ae30b170c8181fde020cee9cb83994176942023abd0c35b0ca571ca0f77a63764b5a170a24f76a4734ef16f858af2950a69b4da1902b8968722e9a328c2f9176d3e71159c82d564e776b8ee6fb648ae94b537ec0efd0898e679d60d230e5f7748a399af565014ddcc22b74b794474155c26c7d02ec9a4180edb2ccd322cd3081a21ed51c0e8e157adb448af052c34dd636a80cb426540cdf0444fcab899105702754b35a95257f9574ab8459a2d20366ed939d280266974f236815603dbc57c250b35dcc0e5a6fa35da21198550625e157282755cfedd0b3f1e1de923dd3f83b1548aeb7411f1e41ae97ca47bb77b467a2462cc8cc8cc1ae95b3edd1c46faee87c1f7e365b7b8782dcbe1a5a7130fa25b94765b32be7029ed5bfeafc40c
	000103
	000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
===================================================================
""".replace("\r\n", "\n"),
            proc.stdout_str)
