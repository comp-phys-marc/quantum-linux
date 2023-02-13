import logging
import feedparser
import ping3, socket

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

SOURCES = [
    "https://github.com/intel/intel-qs/tags.atom",
    "https://github.com/softwareqinc/staq/tags.atom",
    "https://github.com/QuEST-Kit/QuEST/tags.atom",
    "https://github.com/epiqc/ScaffCC/tags.atom",
    "https://github.com/vm6502q/cc65/tags.atom",
    "https://github.com/vm6502q/qsharp-runtime/tags.atom",
    "https://github.com/vm6502q/ProjectQ/tags.atom",
    "https://github.com/vm6502q/qrack-qsharp-runtime/tags.atom",
    "https://github.com/vm6502q/vm6502q/tags.atom",
    "https://github.com/vm6502q/pyqir/tags.atom",
    "http://quantum-studio.net/qx_simulator_linux_x86_64.tar.gz",
    "https://github.com/softwareQinc/qpp/tags.atom",
    "http://www.informatik.uni-bremen.de/agra/eng/qmdd_download.php",
    "https://www.scottaaronson.com/chp/chp.c",
    "https://sourceforge.net/p/eqcs/activity/feed.atom",
    "https://lanq.sourceforge.net/index.php?p=download",
    "http://www.libquantum.de/files/libquantum-1.0.0.tar.gz",
    "https://sourceforge.net/p/qplusplus/activity/feed.atom",
    "https://www.quantware.ups-tlse.fr/QWLIB/fidelity_stat_error.tar.gz",
    "https://www.quantware.ups-tlse.fr/QWLIB/QClib.tar.gz",
    "https://www.quantware.ups-tlse.fr/QWLIB/benenti.tar.gz",
    "https://www.quantware.ups-tlse.fr/QWLIB/benenti2.tar.gz",
    "https://www.quantware.ups-tlse.fr/QWLIB/benenti3.tar.gz",
    "https://www.quantware.ups-tlse.fr/QWLIB/bettelli.tar.gz",
    "https://www.quantware.ups-tlse.fr/QWLIB/harper.tar.gz",
    "https://www.quantware.ups-tlse.fr/QWLIB/giraud.tar.gz",
    "https://www.quantware.ups-tlse.fr/QWLIB/PAREC-Source.tar.gz",
    "https://www.quantware.ups-tlse.fr/bettelli/libquantum-0.6.7.tar.gz",
    "https://www.quantware.ups-tlse.fr/QWLIB/lib_shor.tgz",
    "https://www.quantware.ups-tlse.fr/QWLIB/peachalmers.tgz",
    "https://www.quantware.ups-tlse.fr/QWLIB/lib_pea.tgz",
    "https://www.quantware.ups-tlse.fr/QWLIB/lib_shor2.tgz",
    "https://www.quantware.ups-tlse.fr/QWLIB/brainlinks.tgz",
    "http://thegreves.com/david/software/QDD-0.3.tar.gz",
    "http://hampshire.edu/lspector/qgame++/qgame-0.4.1.tar.gz",
    "https://sourceforge.net/p/qsims/activity/feed.atom",
    "http://web.archive.org/web/20050923134721/http://www.lri.fr/~durr/Attic/qtm/qtm.C",
    "http://tph.tuwien.ac.at/~oemer/tgz/qcl-0.6.7.tgz",
    "https://www-imai.is.s.u-tokyo.ac.jp/~tokunaga/QCS/QCS.tar.gz",
    "https://sourceforge.net/p/qcplusplus/activity/feed.atom",
    "https://sourceforge.net/p/qnc/activity/feed.atom",
    "http://www.ar-tiste.com/Qbtr1-11.tar.gz",
    "https://sourceforge.net/p/qucosi/activity/feed.atom",
    "https://github.com/Marquezino/qwalk/tags.atom",
    "https://quantum-algorithms.herokuapp.com/299/shorsim.tar",
    "https://github.com/vadym-kl/sqct/tags.atom",
    "https://github.com/cda-tum/ddsim/tags.atom",
    "https://github.com/libtangle/qcgpu/tags.atom",
    "https://github.com/comp-phys-marc/qeelibrs/tags.atom"
    # TODO: add all packages in list @ https://quantiki.org/wiki/list-qc-simulators
]

file = open("quantum_packages", "w")
url = ""

for source in SOURCES:

    # a GitHub or SourceForge release feed
    if ".atom" in source:
        try:
            releases = feedparser.parse(source).entries
            release = releases[0]
        
            if "github" in source:
                version = release.id.split("/")[-1]
                url = "/".join(source.split("/")[:-1]) + "/archive/refs/tags/" + version + ".tar.gz"
        
            elif "sourceforge" in source:
                try:
                    latest = "https://sourceforge.net/projects/" +source.split("/")[-3] + "/files/latest/download"
                    ping3.verbose_ping(latest, count=3)
                    url = latest
                except socket.error as e:
                    url = release.link.href
        
        except Exception as e:
            logger.error("Could not parse RSS feed {0}".format(source))
    
    # a direct download link
    else:
        try:
            ping3.verbose_ping(source, count=3)
            url = source
        except socket.error as e:
            logger.error("Could not ping {0}".format(source))

    if url != "":
        logger.info("Found source: {0}".format(url))
        file.write(url + "\r\n")

file.close()
