"""
Open-Source Fully Homomorphic Encryption Library
"""
from __future__ import annotations
import typing
__all__ = ['ADVANCEDSHE', 'AND', 'AP', 'BEHZ', 'BFVRNS_SCHEME', 'BGVRNS_SCHEME', 'BINARY', 'BINFHE_METHOD', 'BINFHE_OUTPUT', 'BINFHE_PARAMSET', 'BINGATE', 'BOOTSTRAPPED', 'BV', 'BinFHEContext', 'CCParamsBFVRNS', 'CCParamsBGVRNS', 'CCParamsCKKSRNS', 'CKKSRNS_SCHEME', 'COEFFICIENT', 'COMPACT', 'COMPRESSION_LEVEL', 'Ciphertext', 'CryptoContext', 'DIVIDE_AND_ROUND_HRA', 'DecryptionNoiseMode', 'DeserializeCiphertext', 'DeserializeCryptoContext', 'DeserializeEvalKey', 'DeserializePrivateKey', 'DeserializePublicKey', 'EVALUATION', 'EXEC_EVALUATION', 'EXEC_NOISE_ESTIMATION', 'EXTENDED', 'EncryptionTechnique', 'EvalKey', 'EvalKeyMap', 'ExecutionMode', 'FHE', 'FHECKKSRNS', 'FIXEDAUTO', 'FIXEDMANUAL', 'FIXED_NOISE_DECRYPT', 'FIXED_NOISE_HRA', 'FIXED_NOISE_MULTIPARTY', 'FLEXIBLEAUTO', 'FLEXIBLEAUTOEXT', 'FRESH', 'Format', 'GAUSSIAN', 'GINX', 'GenCryptoContext', 'GetAllContexts', 'HEStd_128_classic', 'HEStd_192_classic', 'HEStd_256_classic', 'HEStd_NotSet', 'HPS', 'HPSPOVERQ', 'HPSPOVERQLEVELED', 'HYBRID', 'INDCPA', 'INVALID_KS_TECH', 'INVALID_METHOD', 'INVALID_MULTIPARTY_MODE', 'INVALID_OUTPUT', 'INVALID_RS_TECHNIQUE', 'INVALID_SCHEME', 'JSON', 'KEYGEN_MODE', 'KEYSWITCH', 'KeyPair', 'KeySwitchTechnique', 'LEVELEDSHE', 'LMKCDEY', 'LWECiphertext', 'LWEPrivateKey', 'MEDIUM', 'MULTIPARTY', 'MultipartyMode', 'MultiplicationTechnique', 'NAND', 'NOISE_FLOODING_DECRYPT', 'NOISE_FLOODING_HRA', 'NOISE_FLOODING_MULTIPARTY', 'NOR', 'NORESCALE', 'NOT_SET', 'OR', 'PKE', 'PKESchemeFeature', 'PRE', 'PUB_ENCRYPT', 'ParmType', 'Plaintext', 'PrivateKey', 'ProxyReEncryptionMode', 'PublicKey', 'ReleaseAllContexts', 'SCHEME', 'SCHEMESWITCH', 'SERBINARY', 'SERJSON', 'SIGNED_MOD_TEST', 'SLACK', 'SPARSE_TERNARY', 'STANDARD', 'STD128', 'STD128Q', 'STD128Q_3', 'STD128Q_3_LMKCDEY', 'STD128Q_4', 'STD128Q_4_LMKCDEY', 'STD128Q_LMKCDEY', 'STD128_3', 'STD128_3_LMKCDEY', 'STD128_4', 'STD128_4_LMKCDEY', 'STD128_AP', 'STD128_LMKCDEY', 'STD192', 'STD192Q', 'STD192Q_3', 'STD192Q_4', 'STD256', 'STD256Q', 'STD256Q_3', 'STD256Q_4', 'SYM_ENCRYPT', 'ScalingTechnique', 'SecretKeyDist', 'SecurityLevel', 'SerializeToFile', 'TOY', 'UNIFORM_TERNARY', 'XNOR', 'XNOR_FAST', 'XOR', 'XOR_FAST', 'get_native_int']
class BINFHE_METHOD:
    """
    Members:
    
      INVALID_METHOD
    
      AP
    
      GINX
    
      LMKCDEY
    """
    AP: typing.ClassVar[BINFHE_METHOD]  # value = <BINFHE_METHOD.AP: 1>
    GINX: typing.ClassVar[BINFHE_METHOD]  # value = <BINFHE_METHOD.GINX: 2>
    INVALID_METHOD: typing.ClassVar[BINFHE_METHOD]  # value = <BINFHE_METHOD.INVALID_METHOD: 0>
    LMKCDEY: typing.ClassVar[BINFHE_METHOD]  # value = <BINFHE_METHOD.LMKCDEY: 3>
    __members__: typing.ClassVar[dict[str, BINFHE_METHOD]]  # value = {'INVALID_METHOD': <BINFHE_METHOD.INVALID_METHOD: 0>, 'AP': <BINFHE_METHOD.AP: 1>, 'GINX': <BINFHE_METHOD.GINX: 2>, 'LMKCDEY': <BINFHE_METHOD.LMKCDEY: 3>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class BINFHE_OUTPUT:
    """
    Members:
    
      INVALID_OUTPUT
    
      FRESH
    
      BOOTSTRAPPED
    """
    BOOTSTRAPPED: typing.ClassVar[BINFHE_OUTPUT]  # value = <BINFHE_OUTPUT.BOOTSTRAPPED: 2>
    FRESH: typing.ClassVar[BINFHE_OUTPUT]  # value = <BINFHE_OUTPUT.FRESH: 1>
    INVALID_OUTPUT: typing.ClassVar[BINFHE_OUTPUT]  # value = <BINFHE_OUTPUT.INVALID_OUTPUT: 0>
    __members__: typing.ClassVar[dict[str, BINFHE_OUTPUT]]  # value = {'INVALID_OUTPUT': <BINFHE_OUTPUT.INVALID_OUTPUT: 0>, 'FRESH': <BINFHE_OUTPUT.FRESH: 1>, 'BOOTSTRAPPED': <BINFHE_OUTPUT.BOOTSTRAPPED: 2>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class BINFHE_PARAMSET:
    """
    Members:
    
      TOY
    
      MEDIUM
    
      STD128_LMKCDEY
    
      STD128_AP
    
      STD128
    
      STD192
    
      STD256
    
      STD128Q
    
      STD128Q_LMKCDEY
    
      STD192Q
    
      STD256Q
    
      STD128_3
    
      STD128_3_LMKCDEY
    
      STD128Q_3
    
      STD128Q_3_LMKCDEY
    
      STD192Q_3
    
      STD256Q_3
    
      STD128_4
    
      STD128_4_LMKCDEY
    
      STD128Q_4
    
      STD128Q_4_LMKCDEY
    
      STD192Q_4
    
      STD256Q_4
    
      SIGNED_MOD_TEST
    """
    MEDIUM: typing.ClassVar[BINFHE_PARAMSET]  # value = <BINFHE_PARAMSET.MEDIUM: 1>
    SIGNED_MOD_TEST: typing.ClassVar[BINFHE_PARAMSET]  # value = <BINFHE_PARAMSET.SIGNED_MOD_TEST: 23>
    STD128: typing.ClassVar[BINFHE_PARAMSET]  # value = <BINFHE_PARAMSET.STD128: 4>
    STD128Q: typing.ClassVar[BINFHE_PARAMSET]  # value = <BINFHE_PARAMSET.STD128Q: 7>
    STD128Q_3: typing.ClassVar[BINFHE_PARAMSET]  # value = <BINFHE_PARAMSET.STD128Q_3: 13>
    STD128Q_3_LMKCDEY: typing.ClassVar[BINFHE_PARAMSET]  # value = <BINFHE_PARAMSET.STD128Q_3_LMKCDEY: 14>
    STD128Q_4: typing.ClassVar[BINFHE_PARAMSET]  # value = <BINFHE_PARAMSET.STD128Q_4: 19>
    STD128Q_4_LMKCDEY: typing.ClassVar[BINFHE_PARAMSET]  # value = <BINFHE_PARAMSET.STD128Q_4_LMKCDEY: 20>
    STD128Q_LMKCDEY: typing.ClassVar[BINFHE_PARAMSET]  # value = <BINFHE_PARAMSET.STD128Q_LMKCDEY: 8>
    STD128_3: typing.ClassVar[BINFHE_PARAMSET]  # value = <BINFHE_PARAMSET.STD128_3: 11>
    STD128_3_LMKCDEY: typing.ClassVar[BINFHE_PARAMSET]  # value = <BINFHE_PARAMSET.STD128_3_LMKCDEY: 12>
    STD128_4: typing.ClassVar[BINFHE_PARAMSET]  # value = <BINFHE_PARAMSET.STD128_4: 17>
    STD128_4_LMKCDEY: typing.ClassVar[BINFHE_PARAMSET]  # value = <BINFHE_PARAMSET.STD128_4_LMKCDEY: 18>
    STD128_AP: typing.ClassVar[BINFHE_PARAMSET]  # value = <BINFHE_PARAMSET.STD128_AP: 3>
    STD128_LMKCDEY: typing.ClassVar[BINFHE_PARAMSET]  # value = <BINFHE_PARAMSET.STD128_LMKCDEY: 2>
    STD192: typing.ClassVar[BINFHE_PARAMSET]  # value = <BINFHE_PARAMSET.STD192: 5>
    STD192Q: typing.ClassVar[BINFHE_PARAMSET]  # value = <BINFHE_PARAMSET.STD192Q: 9>
    STD192Q_3: typing.ClassVar[BINFHE_PARAMSET]  # value = <BINFHE_PARAMSET.STD192Q_3: 15>
    STD192Q_4: typing.ClassVar[BINFHE_PARAMSET]  # value = <BINFHE_PARAMSET.STD192Q_4: 21>
    STD256: typing.ClassVar[BINFHE_PARAMSET]  # value = <BINFHE_PARAMSET.STD256: 6>
    STD256Q: typing.ClassVar[BINFHE_PARAMSET]  # value = <BINFHE_PARAMSET.STD256Q: 10>
    STD256Q_3: typing.ClassVar[BINFHE_PARAMSET]  # value = <BINFHE_PARAMSET.STD256Q_3: 16>
    STD256Q_4: typing.ClassVar[BINFHE_PARAMSET]  # value = <BINFHE_PARAMSET.STD256Q_4: 22>
    TOY: typing.ClassVar[BINFHE_PARAMSET]  # value = <BINFHE_PARAMSET.TOY: 0>
    __members__: typing.ClassVar[dict[str, BINFHE_PARAMSET]]  # value = {'TOY': <BINFHE_PARAMSET.TOY: 0>, 'MEDIUM': <BINFHE_PARAMSET.MEDIUM: 1>, 'STD128_LMKCDEY': <BINFHE_PARAMSET.STD128_LMKCDEY: 2>, 'STD128_AP': <BINFHE_PARAMSET.STD128_AP: 3>, 'STD128': <BINFHE_PARAMSET.STD128: 4>, 'STD192': <BINFHE_PARAMSET.STD192: 5>, 'STD256': <BINFHE_PARAMSET.STD256: 6>, 'STD128Q': <BINFHE_PARAMSET.STD128Q: 7>, 'STD128Q_LMKCDEY': <BINFHE_PARAMSET.STD128Q_LMKCDEY: 8>, 'STD192Q': <BINFHE_PARAMSET.STD192Q: 9>, 'STD256Q': <BINFHE_PARAMSET.STD256Q: 10>, 'STD128_3': <BINFHE_PARAMSET.STD128_3: 11>, 'STD128_3_LMKCDEY': <BINFHE_PARAMSET.STD128_3_LMKCDEY: 12>, 'STD128Q_3': <BINFHE_PARAMSET.STD128Q_3: 13>, 'STD128Q_3_LMKCDEY': <BINFHE_PARAMSET.STD128Q_3_LMKCDEY: 14>, 'STD192Q_3': <BINFHE_PARAMSET.STD192Q_3: 15>, 'STD256Q_3': <BINFHE_PARAMSET.STD256Q_3: 16>, 'STD128_4': <BINFHE_PARAMSET.STD128_4: 17>, 'STD128_4_LMKCDEY': <BINFHE_PARAMSET.STD128_4_LMKCDEY: 18>, 'STD128Q_4': <BINFHE_PARAMSET.STD128Q_4: 19>, 'STD128Q_4_LMKCDEY': <BINFHE_PARAMSET.STD128Q_4_LMKCDEY: 20>, 'STD192Q_4': <BINFHE_PARAMSET.STD192Q_4: 21>, 'STD256Q_4': <BINFHE_PARAMSET.STD256Q_4: 22>, 'SIGNED_MOD_TEST': <BINFHE_PARAMSET.SIGNED_MOD_TEST: 23>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class BINGATE:
    """
    Members:
    
      OR
    
      AND
    
      NOR
    
      NAND
    
      XOR_FAST
    
      XNOR_FAST
    
      XOR
    
      XNOR
    """
    AND: typing.ClassVar[BINGATE]  # value = <BINGATE.AND: 1>
    NAND: typing.ClassVar[BINGATE]  # value = <BINGATE.NAND: 3>
    NOR: typing.ClassVar[BINGATE]  # value = <BINGATE.NOR: 2>
    OR: typing.ClassVar[BINGATE]  # value = <BINGATE.OR: 0>
    XNOR: typing.ClassVar[BINGATE]  # value = <BINGATE.XNOR: 5>
    XNOR_FAST: typing.ClassVar[BINGATE]  # value = <BINGATE.XNOR_FAST: 12>
    XOR: typing.ClassVar[BINGATE]  # value = <BINGATE.XOR: 4>
    XOR_FAST: typing.ClassVar[BINGATE]  # value = <BINGATE.XOR_FAST: 11>
    __members__: typing.ClassVar[dict[str, BINGATE]]  # value = {'OR': <BINGATE.OR: 0>, 'AND': <BINGATE.AND: 1>, 'NOR': <BINGATE.NOR: 2>, 'NAND': <BINGATE.NAND: 3>, 'XOR_FAST': <BINGATE.XOR_FAST: 11>, 'XNOR_FAST': <BINGATE.XNOR_FAST: 12>, 'XOR': <BINGATE.XOR: 4>, 'XNOR': <BINGATE.XNOR: 5>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class BinFHEContext:
    def BTKeyGen(self, sk: ..., keygenMode: KEYGEN_MODE = ...) -> None:
        """
            Generates bootstrapping keys.
        
            :param sk: The secret key.
            :type sk: LWEPrivateKey
        """
    def Decrypt(self, sk: ..., ct: ..., p: int = 4) -> int:
        """
            Decrypts a ciphertext using a secret key.
        
            :param sk: The secret key.
            :type sk: LWEPrivateKey
            :param ct: The ciphertext.
            :type ct: LWECiphertext
            :param p: Plaintext modulus (default 4).
            :type p: int
            :return: The plaintext.
            :rtype: int
        """
    def Encrypt(self, sk: ..., m: int, output: BINFHE_OUTPUT = ..., p: int = 4, mod: int = 0) -> ...:
        """
            Encrypts a bit or integer using a secret key (symmetric key encryption).
        
            :param sk: The secret key.
            :type sk: LWEPrivateKey
            :param m: The plaintext.
            :type m: int
            :param output: FRESH to generate a fresh ciphertext, BOOTSTRAPPED to generate a refreshed ciphertext (default).
            :type output: BINFHE_OUTPUT
            :param p: Plaintext modulus (default 4).
            :type p: int
            :param mod: Encrypt according to mod instead of m_q if mod != 0.
            :type mod: int
            :return: The ciphertext.
            :rtype: LWECiphertext
        """
    def EvalBinGate(self, gate: BINGATE, ct1: ..., ct2: ...) -> ...:
        """
            Evaluates a binary gate (calls bootstrapping as a subroutine).
        
            :param gate: The gate; can be AND, OR, NAND, NOR, XOR, or XNOR.
            :type gate: BINGATE
            :param ct1: First ciphertext.
            :type ct1: LWECiphertext
            :param ct2: Second ciphertext.
            :type ct2: LWECiphertext
            :return: The resulting ciphertext.
            :rtype: LWECiphertext
        """
    def EvalDecomp(self, ct: ...) -> list[...]:
        """
            Evaluate ciphertext decomposition
        
            :param ct: ciphertext to be bootstrapped
            :type ct: LWECiphertext
            :return: a list with the resulting ciphertexts
            :rtype: List[LWECiphertext]
        """
    def EvalFloor(self, ct: ..., roundbits: int = 0) -> ...:
        """
            Evaluate a round down function
        
            :param ct: ciphertext to be bootstrapped
            :type ct: LWECiphertext
            :param roundbits: number of bits to be rounded
            :type roundbits: int
            :return: the resulting ciphertext
            :rtype: LWECiphertext
        """
    def EvalFunc(self, ct: ..., LUT: list[int]) -> ...:
        """
            Evaluate an arbitrary function
        
            :param ct: ciphertext to be bootstrapped
            :type ct: LWECiphertext
            :param LUT: the look-up table of the to-be-evaluated function
            :type LUT: List[int]
            :return: the resulting ciphertext
            :rtype: LWECiphertext
        """
    def EvalNOT(self, ct: ...) -> ...:
        """
            Evaluates the NOT gate.
        
            :param ct: The input ciphertext.
            :type ct: LWECiphertext
            :return: The resulting ciphertext.
            :rtype: LWECiphertext
        """
    def EvalSign(self, ct: ..., schemeSwitch: bool = False) -> ...:
        """
            Evaluate a sign function over large precisions
        
            :param ct: ciphertext to be bootstrapped
            :type ct: LWECiphertext
            :param schemeSwitch: flag that indicates if it should be compatible to scheme switching
            :type schemeSwitch: bool
            :return: the resulting ciphertext
            :rtype: LWECiphertext
        """
    @typing.overload
    def GenerateBinFHEContext(self, set: BINFHE_PARAMSET, method: BINFHE_METHOD = ...) -> None:
        """
            Creates a crypto context using predefined parameters sets. Recommended for most users.
        
            :param set: the parameter set: TOY, MEDIUM, STD128, STD192, STD256 with variants
            :type set: BINFHE_PARAMSET
            :param method: the bootstrapping method (DM or CGGI or LMKCDEY)
            :type method: BINFHE_METHOD
            :return: The created crypto context.
            :rtype: BinFHEContext
        """
    @typing.overload
    def GenerateBinFHEContext(self, set: BINFHE_PARAMSET, arbFunc: bool, logQ: int = 11, N: int = 0, method: BINFHE_METHOD = ..., timeOptimization: bool = False) -> None:
        """
            Creates a crypto context using custom parameters. Should be used with care (only for advanced users familiar with LWE parameter selection).
        
            :param set: The parameter set: TOY, MEDIUM, STD128, STD192, STD256 with variants.
            :type set: BINFHE_PARAMSET
            :param arbFunc:  whether need to evaluate an arbitrary function using functional bootstrapping
            :type arbFunc: bool
            :param logQ:  log(input ciphertext modulus)
            :type logQ: int
            :param N:  ring dimension for RingGSW/RLWE used in bootstrapping
            :type N: int
            :param method: the bootstrapping method (DM or CGGI or LMKCDEY)
            :type method: BINFHE_METHOD
            :param timeOptimization:  whether to use dynamic bootstrapping technique
            :type timeOptimization: bool
            :return: creates the cryptocontext.
            :rtype: BinFHEContext
        """
    def GenerateLUTviaFunction(self, f: typing.Callable, p: int) -> list[int]:
        """
            Generate the LUT for the to-be-evaluated function
        
            :param f: the to-be-evaluated function on an integer message and a plaintext modulus
            :type f: function(int, int) -> int
            :param p: plaintext modulus
            :type p: int
            :return: the resulting ciphertext
            :rtype: List[int]
        """
    def GetBeta(self) -> int:
        ...
    def GetMaxPlaintextSpace(self) -> int:
        ...
    def Getn(self) -> int:
        ...
    def Getq(self) -> int:
        ...
    def KeyGen(self) -> ...:
        """
            Generates a secret key for the main LWE scheme.
        
            :return: The secret key.
            :rtype: LWEPrivateKey
        """
    def __init__(self) -> None:
        ...
class CCParamsBFVRNS:
    def GetBatchSize(self) -> int:
        ...
    def GetDecryptionNoiseMode(self) -> DecryptionNoiseMode:
        ...
    def GetDesiredPrecision(self) -> float:
        ...
    def GetDigitSize(self) -> int:
        ...
    def GetEncryptionTechnique(self) -> EncryptionTechnique:
        ...
    def GetEvalAddCount(self) -> int:
        ...
    def GetExecutionMode(self) -> ExecutionMode:
        ...
    def GetFirstModSize(self) -> int:
        ...
    def GetInteractiveBootCompressionLevel(self) -> COMPRESSION_LEVEL:
        ...
    def GetKeySwitchCount(self) -> int:
        ...
    def GetKeySwitchTechnique(self) -> KeySwitchTechnique:
        ...
    def GetMaxRelinSkDeg(self) -> int:
        ...
    def GetMultiHopModSize(self) -> int:
        ...
    def GetMultipartyMode(self) -> MultipartyMode:
        ...
    def GetMultiplicationTechnique(self) -> MultiplicationTechnique:
        ...
    def GetMultiplicativeDepth(self) -> int:
        ...
    def GetNoiseEstimate(self) -> float:
        ...
    def GetNumAdversarialQueries(self) -> float:
        ...
    def GetNumLargeDigits(self) -> int:
        ...
    def GetPREMode(self) -> ProxyReEncryptionMode:
        ...
    def GetPlaintextModulus(self) -> int:
        ...
    def GetRingDim(self) -> int:
        ...
    def GetScalingModSize(self) -> int:
        ...
    def GetScalingTechnique(self) -> ScalingTechnique:
        ...
    def GetScheme(self) -> SCHEME:
        ...
    def GetSecretKeyDist(self) -> SecretKeyDist:
        ...
    def GetSecurityLevel(self) -> SecurityLevel:
        ...
    def GetStandardDeviation(self) -> float:
        ...
    def GetStatisticalSecurity(self) -> float:
        ...
    def SetBatchSize(self, arg0: int) -> None:
        ...
    def SetDecryptionNoiseMode(self, arg0: DecryptionNoiseMode) -> None:
        ...
    def SetDesiredPrecision(self, arg0: float) -> None:
        ...
    def SetDigitSize(self, arg0: int) -> None:
        ...
    def SetEncryptionTechnique(self, arg0: EncryptionTechnique) -> None:
        ...
    def SetEvalAddCount(self, arg0: int) -> None:
        ...
    def SetExecutionMode(self, arg0: ExecutionMode) -> None:
        ...
    def SetFirstModSize(self, arg0: int) -> None:
        ...
    def SetInteractiveBootCompressionLevel(self, arg0: COMPRESSION_LEVEL) -> None:
        ...
    def SetKeySwitchCount(self, arg0: int) -> None:
        ...
    def SetKeySwitchTechnique(self, arg0: KeySwitchTechnique) -> None:
        ...
    def SetMaxRelinSkDeg(self, arg0: int) -> None:
        ...
    def SetMultiHopModSize(self, arg0: int) -> None:
        ...
    def SetMultipartyMode(self, arg0: MultipartyMode) -> None:
        ...
    def SetMultiplicationTechnique(self, arg0: MultiplicationTechnique) -> None:
        ...
    def SetMultiplicativeDepth(self, arg0: int) -> None:
        ...
    def SetNoiseEstimate(self, arg0: float) -> None:
        ...
    def SetNumAdversarialQueries(self, arg0: int) -> None:
        ...
    def SetNumLargeDigits(self, arg0: int) -> None:
        ...
    def SetPREMode(self, arg0: ProxyReEncryptionMode) -> None:
        ...
    def SetPlaintextModulus(self, arg0: int) -> None:
        ...
    def SetRingDim(self, arg0: int) -> None:
        ...
    def SetScalingModSize(self, arg0: int) -> None:
        ...
    def SetScalingTechnique(self, arg0: ScalingTechnique) -> None:
        ...
    def SetSecretKeyDist(self, arg0: SecretKeyDist) -> None:
        ...
    def SetSecurityLevel(self, arg0: SecurityLevel) -> None:
        ...
    def SetStandardDeviation(self, arg0: float) -> None:
        ...
    def SetStatisticalSecurity(self, arg0: int) -> None:
        ...
    def SetThresholdNumOfParties(self, arg0: int) -> None:
        ...
    def __init__(self) -> None:
        ...
    def __str__(self) -> str:
        ...
class CCParamsBGVRNS:
    def GetBatchSize(self) -> int:
        ...
    def GetDecryptionNoiseMode(self) -> DecryptionNoiseMode:
        ...
    def GetDesiredPrecision(self) -> float:
        ...
    def GetDigitSize(self) -> int:
        ...
    def GetEncryptionTechnique(self) -> EncryptionTechnique:
        ...
    def GetEvalAddCount(self) -> int:
        ...
    def GetExecutionMode(self) -> ExecutionMode:
        ...
    def GetFirstModSize(self) -> int:
        ...
    def GetInteractiveBootCompressionLevel(self) -> COMPRESSION_LEVEL:
        ...
    def GetKeySwitchCount(self) -> int:
        ...
    def GetKeySwitchTechnique(self) -> KeySwitchTechnique:
        ...
    def GetMaxRelinSkDeg(self) -> int:
        ...
    def GetMultiHopModSize(self) -> int:
        ...
    def GetMultipartyMode(self) -> MultipartyMode:
        ...
    def GetMultiplicationTechnique(self) -> MultiplicationTechnique:
        ...
    def GetMultiplicativeDepth(self) -> int:
        ...
    def GetNoiseEstimate(self) -> float:
        ...
    def GetNumAdversarialQueries(self) -> float:
        ...
    def GetNumLargeDigits(self) -> int:
        ...
    def GetPREMode(self) -> ProxyReEncryptionMode:
        ...
    def GetPlaintextModulus(self) -> int:
        ...
    def GetRingDim(self) -> int:
        ...
    def GetScalingModSize(self) -> int:
        ...
    def GetScalingTechnique(self) -> ScalingTechnique:
        ...
    def GetScheme(self) -> SCHEME:
        ...
    def GetSecretKeyDist(self) -> SecretKeyDist:
        ...
    def GetSecurityLevel(self) -> SecurityLevel:
        ...
    def GetStandardDeviation(self) -> float:
        ...
    def GetStatisticalSecurity(self) -> float:
        ...
    def SetBatchSize(self, arg0: int) -> None:
        ...
    def SetDecryptionNoiseMode(self, arg0: DecryptionNoiseMode) -> None:
        ...
    def SetDesiredPrecision(self, arg0: float) -> None:
        ...
    def SetDigitSize(self, arg0: int) -> None:
        ...
    def SetEncryptionTechnique(self, arg0: EncryptionTechnique) -> None:
        ...
    def SetEvalAddCount(self, arg0: int) -> None:
        ...
    def SetExecutionMode(self, arg0: ExecutionMode) -> None:
        ...
    def SetFirstModSize(self, arg0: int) -> None:
        ...
    def SetInteractiveBootCompressionLevel(self, arg0: COMPRESSION_LEVEL) -> None:
        ...
    def SetKeySwitchCount(self, arg0: int) -> None:
        ...
    def SetKeySwitchTechnique(self, arg0: KeySwitchTechnique) -> None:
        ...
    def SetMaxRelinSkDeg(self, arg0: int) -> None:
        ...
    def SetMultiHopModSize(self, arg0: int) -> None:
        ...
    def SetMultipartyMode(self, arg0: MultipartyMode) -> None:
        ...
    def SetMultiplicationTechnique(self, arg0: MultiplicationTechnique) -> None:
        ...
    def SetMultiplicativeDepth(self, arg0: int) -> None:
        ...
    def SetNoiseEstimate(self, arg0: float) -> None:
        ...
    def SetNumAdversarialQueries(self, arg0: int) -> None:
        ...
    def SetNumLargeDigits(self, arg0: int) -> None:
        ...
    def SetPREMode(self, arg0: ProxyReEncryptionMode) -> None:
        ...
    def SetPlaintextModulus(self, arg0: int) -> None:
        ...
    def SetRingDim(self, arg0: int) -> None:
        ...
    def SetScalingModSize(self, arg0: int) -> None:
        ...
    def SetScalingTechnique(self, arg0: ScalingTechnique) -> None:
        ...
    def SetSecretKeyDist(self, arg0: SecretKeyDist) -> None:
        ...
    def SetSecurityLevel(self, arg0: SecurityLevel) -> None:
        ...
    def SetStandardDeviation(self, arg0: float) -> None:
        ...
    def SetStatisticalSecurity(self, arg0: int) -> None:
        ...
    def SetThresholdNumOfParties(self, arg0: int) -> None:
        ...
    def __init__(self) -> None:
        ...
    def __str__(self) -> str:
        ...
class CCParamsCKKSRNS:
    def GetBatchSize(self) -> int:
        ...
    def GetDecryptionNoiseMode(self) -> DecryptionNoiseMode:
        ...
    def GetDesiredPrecision(self) -> float:
        ...
    def GetDigitSize(self) -> int:
        ...
    def GetEncryptionTechnique(self) -> EncryptionTechnique:
        ...
    def GetEvalAddCount(self) -> int:
        ...
    def GetExecutionMode(self) -> ExecutionMode:
        ...
    def GetFirstModSize(self) -> int:
        ...
    def GetInteractiveBootCompressionLevel(self) -> COMPRESSION_LEVEL:
        ...
    def GetKeySwitchCount(self) -> int:
        ...
    def GetKeySwitchTechnique(self) -> KeySwitchTechnique:
        ...
    def GetMaxRelinSkDeg(self) -> int:
        ...
    def GetMultiHopModSize(self) -> int:
        ...
    def GetMultipartyMode(self) -> MultipartyMode:
        ...
    def GetMultiplicationTechnique(self) -> MultiplicationTechnique:
        ...
    def GetMultiplicativeDepth(self) -> int:
        ...
    def GetNoiseEstimate(self) -> float:
        ...
    def GetNumAdversarialQueries(self) -> float:
        ...
    def GetNumLargeDigits(self) -> int:
        ...
    def GetPREMode(self) -> ProxyReEncryptionMode:
        ...
    def GetPlaintextModulus(self) -> int:
        ...
    def GetRingDim(self) -> int:
        ...
    def GetScalingModSize(self) -> int:
        ...
    def GetScalingTechnique(self) -> ScalingTechnique:
        ...
    def GetScheme(self) -> SCHEME:
        ...
    def GetSecretKeyDist(self) -> SecretKeyDist:
        ...
    def GetSecurityLevel(self) -> SecurityLevel:
        ...
    def GetStandardDeviation(self) -> float:
        ...
    def GetStatisticalSecurity(self) -> float:
        ...
    def SetBatchSize(self, arg0: int) -> None:
        ...
    def SetDecryptionNoiseMode(self, arg0: DecryptionNoiseMode) -> None:
        ...
    def SetDesiredPrecision(self, arg0: float) -> None:
        ...
    def SetDigitSize(self, arg0: int) -> None:
        ...
    def SetEncryptionTechnique(self, arg0: EncryptionTechnique) -> None:
        ...
    def SetEvalAddCount(self, arg0: int) -> None:
        ...
    def SetExecutionMode(self, arg0: ExecutionMode) -> None:
        ...
    def SetFirstModSize(self, arg0: int) -> None:
        ...
    def SetInteractiveBootCompressionLevel(self, arg0: COMPRESSION_LEVEL) -> None:
        ...
    def SetKeySwitchCount(self, arg0: int) -> None:
        ...
    def SetKeySwitchTechnique(self, arg0: KeySwitchTechnique) -> None:
        ...
    def SetMaxRelinSkDeg(self, arg0: int) -> None:
        ...
    def SetMultiHopModSize(self, arg0: int) -> None:
        ...
    def SetMultipartyMode(self, arg0: MultipartyMode) -> None:
        ...
    def SetMultiplicationTechnique(self, arg0: MultiplicationTechnique) -> None:
        ...
    def SetMultiplicativeDepth(self, arg0: int) -> None:
        ...
    def SetNoiseEstimate(self, arg0: float) -> None:
        ...
    def SetNumAdversarialQueries(self, arg0: int) -> None:
        ...
    def SetNumLargeDigits(self, arg0: int) -> None:
        ...
    def SetPREMode(self, arg0: ProxyReEncryptionMode) -> None:
        ...
    def SetPlaintextModulus(self, arg0: int) -> None:
        ...
    def SetRingDim(self, arg0: int) -> None:
        ...
    def SetScalingModSize(self, arg0: int) -> None:
        ...
    def SetScalingTechnique(self, arg0: ScalingTechnique) -> None:
        ...
    def SetSecretKeyDist(self, arg0: SecretKeyDist) -> None:
        ...
    def SetSecurityLevel(self, arg0: SecurityLevel) -> None:
        ...
    def SetStandardDeviation(self, arg0: float) -> None:
        ...
    def SetStatisticalSecurity(self, arg0: int) -> None:
        ...
    def SetThresholdNumOfParties(self, arg0: int) -> None:
        ...
    def __init__(self) -> None:
        ...
    def __str__(self) -> str:
        ...
class COMPRESSION_LEVEL:
    """
    Members:
    
      COMPACT
    
      SLACK
    """
    COMPACT: typing.ClassVar[COMPRESSION_LEVEL]  # value = <COMPRESSION_LEVEL.COMPACT: 2>
    SLACK: typing.ClassVar[COMPRESSION_LEVEL]  # value = <COMPRESSION_LEVEL.SLACK: 3>
    __members__: typing.ClassVar[dict[str, COMPRESSION_LEVEL]]  # value = {'COMPACT': <COMPRESSION_LEVEL.COMPACT: 2>, 'SLACK': <COMPRESSION_LEVEL.SLACK: 3>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class Ciphertext:
    def Clone(self) -> Ciphertext:
        ...
    def GetLevel(self) -> int:
        """
            Get the number of scalings performed.
        
            :return: The level of the ciphertext.
            :rtype: int
        """
    def GetSlots(self) -> int:
        ...
    def RemoveElement(self, arg0: int) -> None:
        """
            Remove an element from the ciphertext inner vector given its index.
        
            :param index: The index of the element to remove.
            :type index: int
        """
    def SetLevel(self, level: int) -> None:
        """
            Set the number of scalings.
        
            :param level: The level to set.
            :type level: int
        """
    def SetSlots(self, arg0: int) -> None:
        ...
    def __add__(self, arg0: Ciphertext) -> Ciphertext:
        ...
    def __init__(self) -> None:
        ...
class CryptoContext:
    @staticmethod
    def ClearEvalAutomorphismKeys() -> None:
        """
            ClearEvalAutomorphismKeys - flush EvalAutomorphismKey cache
        """
    @staticmethod
    def ClearEvalMultKeys() -> None:
        """
            ClearEvalMultKeys - flush EvalMultKey cache for a given id
        
            :param id: the corresponding key id
            :type id: str
        """
    @staticmethod
    @typing.overload
    def DeserializeEvalAutomorphismKey(filename: str, sertype: SERBINARY) -> bool:
        """
            DeserializeEvalAutomorphismKey deserialize all keys in the serialization deserialized keys silently replace any existing matching keys deserialization will create CryptoContext if necessary
        
            :param filename: path for the file to deserialize from
            :type filename: str
            :param sertype: type of serialization
            :type sertype: SERJSON, SERBINARY
            :return: bool: true on success
        """
    @staticmethod
    @typing.overload
    def DeserializeEvalAutomorphismKey(filename: str, sertype: SERJSON) -> bool:
        """
            DeserializeEvalAutomorphismKey deserialize all keys in the serialization deserialized keys silently replace any existing matching keys deserialization will create CryptoContext if necessary
        
            :param filename: path for the file to deserialize from
            :type filename: str
            :param sertype: type of serialization
            :type sertype: SERJSON, SERBINARY
            :return: bool: true on success
        """
    @staticmethod
    @typing.overload
    def DeserializeEvalMultKey(filename: str, sertype: SERBINARY) -> bool:
        """
            DeserializeEvalMultKey deserialize all keys in the serialization deserialized keys silently replace any existing matching keys deserialization will create CryptoContext if necessary
        
            :param filename: path for the file to deserialize from
            :type filename: str
            :param sertype: type of serialization
            :type sertype: SERJSON, SERBINARY
            :return: bool: true on success
        """
    @staticmethod
    @typing.overload
    def DeserializeEvalMultKey(filename: str, sertype: SERJSON) -> bool:
        """
            DeserializeEvalMultKey deserialize all keys in the serialization deserialized keys silently replace any existing matching keys deserialization will create CryptoContext if necessary
        
            :param filename: path for the file to deserialize from
            :type filename: str
            :param sertype: type of serialization
            :type sertype: SERJSON, SERBINARY
            :return: bool: true on success
        """
    @staticmethod
    def InsertEvalMultKey(evalKeyVec: list[EvalKey]) -> None:
        """
            InsertEvalMultKey - add the given vector of keys to the map, replacing the existing vector if there
        
            :param evalKeyVec: vector of keys
            :type evalKeyVec: List[EvalKey]
        """
    @staticmethod
    def InsertEvalSumKey(evalKeyMap: EvalKeyMap) -> None:
        """
            InsertEvalSumKey - add the given map of keys to the map, replacing the existing map if there
        
            :param evalKeyMap: key map
            :type evalKeyMap: EvalKeyMap
        """
    @staticmethod
    @typing.overload
    def SerializeEvalAutomorphismKey(filename: str, sertype: SERBINARY, id: str = '') -> bool:
        """
            SerializeEvalAutomorphismKey for a single EvalAuto key or all of the EvalAuto keys
        
            :param filename: output file
            :type filename: str
            :param sertype: serialization type
            :type sertype: SERJSON, SERBINARY
            :param id: key to serialize; empty string means all keys
            :type id: str
            :return: bool: true on success
        """
    @staticmethod
    @typing.overload
    def SerializeEvalAutomorphismKey(filename: str, sertype: SERJSON, id: str = '') -> bool:
        """
            SerializeEvalAutomorphismKey for a single EvalAuto key or all of the EvalAuto keys
        
            :param filename: output file
            :type filename: str
            :param sertype: serialization type
            :type sertype: SERJSON, SERBINARY
            :param id: key to serialize; empty string means all keys
            :type id: str
            :return: bool: true on success
        """
    @staticmethod
    @typing.overload
    def SerializeEvalMultKey(filename: str, sertype: SERBINARY, id: str = '') -> bool:
        """
            SerializeEvalMultKey for a single EvalMult key or all of the EvalMult keys
        
            :param filename: output file to serialize to
            :type filename: str
            :param sertype: type of serialization
            :type sertype: SERJSON, SERBINARY
            :param id: for key to serialize - if empty string, serialize them all
            :type id: str
            :return: bool: true on success (false on failure or no keys found)
        """
    @staticmethod
    @typing.overload
    def SerializeEvalMultKey(filename: str, sertype: SERJSON, id: str = '') -> bool:
        """
            SerializeEvalMultKey for a single EvalMult key or all of the EvalMult keys
        
            :param filename: output file to serialize to
            :type filename: str
            :param sertype: type of serialization
            :type sertype: SERJSON, SERBINARY
            :param id: for key to serialize - if empty string, serialize them all
            :type id: str
            :return: bool: true on success (false on failure or no keys found)
        """
    @typing.overload
    def Decrypt(self, privateKey: PrivateKey, ciphertext: Ciphertext) -> Plaintext:
        """
        Decrypt a single ciphertext into the appropriate plaintext
        
        :param ciphertext: ciphertext to decrypt
        :type ciphertext: Ciphertext
        :param privateKey: decryption key
        :type privateKey: PrivateKey
        :return: decrypted plaintext
        :rtype: Plaintext
        """
    @typing.overload
    def Decrypt(self, ciphertext: Ciphertext, privateKey: PrivateKey) -> Plaintext:
        """
        Decrypt a single ciphertext into the appropriate plaintext
        
        :param ciphertext: ciphertext to decrypt
        :type ciphertext: Ciphertext
        :param privateKey: decryption key
        :type privateKey: PrivateKey
        :return: decrypted plaintext
        :rtype: Plaintext
        """
    def Enable(self, feature: PKESchemeFeature) -> None:
        """
            Enable a particular feature for use with this CryptoContext
        
            :param feature: the feature that should be enabled. 
                            The list of available features is defined in the PKESchemeFeature enum.
            :type feature: PKESchemeFeature
        """
    def Encrypt(self, publicKey: PublicKey, plaintext: Plaintext) -> Ciphertext:
        """
            Encrypt a plaintext using a given public key
        
            :param plaintext: plaintext
            :type plaintext: Plaintext
            :param publicKey: public key
            :type publicKey: PublicKey
            :return: ciphertext (or null on failure)
            :rtype: Ciphertext
        """
    @typing.overload
    def EvalAdd(self, ciphertext1: Ciphertext, ciphertext2: Ciphertext) -> Ciphertext:
        """
        Homomorphic addition of two ciphertexts
        
        :param ciphertext1: first addend
        :type ciphertext1: Ciphertext
        :param ciphertext2: second addend
        :type ciphertext2: Ciphertext
        :return: the result as a new ciphertext
        :rtype: Ciphertext
        """
    @typing.overload
    def EvalAdd(self, ciphertext: Ciphertext, constant: float) -> Ciphertext:
        """
        EvalAdd - OpenFHE EvalAdd method for a ciphertext and a real number. Supported only in CKKS.
        
        :param ciphertext: input ciphertext
        :type ciphertext: Ciphertext
        :param constant: a real number
        :type constant: float
        :return: new ciphertext for ciphertext + constant
        :rtype: Ciphertext
        """
    @typing.overload
    def EvalAdd(self, ciphertext: Ciphertext, plaintext: Plaintext) -> Ciphertext:
        """
        EvalAdd - OpenFHE EvalAdd method for a ciphertext and plaintext
        
        :param ciphertext: input ciphertext
        :type ciphertext: Ciphertext
        :param plaintex: input plaintext
        :type plaintext: Plaintext
        :return: new ciphertext for ciphertext + constant
        :rtype: Ciphertext
        """
    @typing.overload
    def EvalAddInPlace(self, ciphertext1: Ciphertext, ciphertext2: Ciphertext) -> None:
        """
        In-place homomorphic addition of two ciphertexts
        
        :param ciphertext1: ciphertext1
        :type ciphertext1: Ciphertext
        :param ciphertext2: second addend
        :type ciphertext2: Ciphertext
        :return: ciphertext1 contains ciphertext1 + ciphertext2
        """
    @typing.overload
    def EvalAddInPlace(self, ciphertext: Ciphertext, plaintext: Plaintext) -> None:
        """
        In-place addition for a ciphertext and plaintext
        
        :param ciphertext: Input/output ciphertext
        :type ciphertext: Ciphertext
        :param plaintext: Input plaintext
        :type plaintext: Plaintext
        :return: ciphertext contains ciphertext + plaintext
        """
    @typing.overload
    def EvalAddInPlace(self, plaintext: Plaintext, ciphertext: Ciphertext) -> None:
        ...
    @typing.overload
    def EvalAddMutable(self, ciphertext1: Ciphertext, ciphertext2: Ciphertext) -> Ciphertext:
        """
        Homomorphic addition of two mutable ciphertexts (they can be changed during the operation)
        
        :param ciphertext1: first addend
        :type ciphertext1: Ciphertext
        :param ciphertext2: second addend
        :type ciphertext2: Ciphertext
        :return: the result as a new ciphertext
        :rtype: Ciphertext
        """
    @typing.overload
    def EvalAddMutable(self, ciphertext: Ciphertext, plaintext: Plaintext) -> Ciphertext:
        """
        Homomorphic addition a mutable ciphertext and plaintext
        
        :param ciphertext: ciphertext
        :type ciphertext: Ciphertext
        :param plaintext: plaintext
        :type plaintext: Plaintext
        :return: new ciphertext for ciphertext + plaintext
        :rtype: Ciphertext
        """
    @typing.overload
    def EvalAddMutable(self, plaintext: Plaintext, ciphertext: Ciphertext) -> Ciphertext:
        ...
    def EvalAddMutableInPlace(self, ciphertext1: Ciphertext, ciphertext2: Ciphertext) -> None:
        """
            Homomorphic addition a mutable ciphertext and plaintext
        
            :param ciphertext1: first addend
            :type ciphertext1: Ciphertext
            :param ciphertext2: second addend
            :type ciphertext2: Ciphertext
            :return: ciphertext1 contains ciphertext1 + ciphertext2
        """
    def EvalAtIndex(self, ciphertext: Ciphertext, index: int) -> Ciphertext:
        """
            Rotates a ciphertext by an index (positive index is a left shift, negative index is a right shift). Uses a rotation key stored in a crypto context.
        
            :param ciphertext: input ciphertext
            :type ciphertext: Ciphertext
            :param i: rotation index
            :type i: int
            :return: a rotated ciphertext
            :rtype: Ciphertext
        """
    def EvalAtIndexKeyGen(self, privateKey: PrivateKey, indexList: list[int], publicKey: PublicKey = None) -> None:
        """
            EvalAtIndexKeyGen generates evaluation keys for a list of rotation indices
        
            :param privateKey: the private key
            :type privateKey: PrivateKey
            :param indexList: list of indices
            :type indexList: list
            :param publicKey: the public key (used in NTRU schemes). Not used anymore.
            :type publicKey: PublicKey
            :return: None
        """
    @typing.overload
    def EvalAutomorphismKeyGen(self, privateKey: PrivateKey, indexList: list[int]) -> EvalKeyMap:
        """
            Generate automophism keys for a given private key; Uses the private key for encryption
        
            :param privateKey: private key.
            :type privateKey: PrivateKey
            :param indexList: list of automorphism indices to be computed.
            :type indexList: list
            :return: returns the evaluation key
            :rtype: EvalKeyMap
        """
    @typing.overload
    def EvalAutomorphismKeyGen(self, publicKey: PublicKey, privateKey: PrivateKey, indexList: list[int]) -> EvalKeyMap:
        """
            NOT USED BY ANY CRYPTO SCHEME: Generate automophism keys for a public and private key
        """
    def EvalBootstrap(self, ciphertext: Ciphertext, numIterations: int = 1, precision: int = 0) -> Ciphertext:
        """
            Defines the bootstrapping evaluation of ciphertext using either the FFT-like method or the linear method
        
            :param ciphertext: the input ciphertext
            :type ciphertext: Ciphertext
            :param numIterations: number of iterations to run iterative bootstrapping (Meta-BTS). Increasing the iterations increases the precision of bootstrapping
            :type numIterations: int
            :param precision: precision of initial bootstrapping algorithm. This value is determined by the user experimentally by first running EvalBootstrap with numIterations = 1 and precision = 0 (unused).
            :type precision: int
            :return: Ciphertext: the refreshed ciphertext
            :rtype: Ciphertext
        """
    def EvalBootstrapKeyGen(self, privateKey: PrivateKey, slots: int) -> None:
        """
            Generates all automorphism keys for EvalBootstrap. Supported in CKKS only. EvalBootstrapKeyGen uses the baby-step/giant-step strategy.
        
            :param privateKey: private key.
            :type privateKey: PrivateKey
            :param slots: number of slots to support permutations on.
            :type slots: int
            :return: None
        """
    def EvalBootstrapSetup(self, levelBudget: list[int] = [5, 4], dim1: list[int] = [0, 0], slots: int = 0, correctionFactor: int = 0, precompute: bool = True) -> None:
        """
            Bootstrap functionality: There are three methods that have to be called in this specific order:
        
            1. EvalBootstrapSetup: computes and encodes the coefficients for encoding and decoding and stores the necessary parameters
        
            2. EvalBootstrapKeyGen: computes and stores the keys for rotations and conjugation
        
            3. EvalBootstrap: refreshes the given ciphertext Sets all parameters for both linear and FTT-like methods. Supported in CKKS only.
        
            :param levelBudget: vector of budgets for the amount of levels in encoding and decoding
            :type levelBudget: list
            :param dim1: vector of inner dimension in the baby-step giant-step routine for encoding and decodingl
            :type dim1: list
            :param slots: number of slots to be bootstraped
            :type slots: int
            :param correctionFactor: value to internally rescale message by to improve precision of bootstrapping. If set to 0, we use the default logic. This value is only used when NATIVE_SIZE=64.
            :type correctionFactor: int
            :return: None
        """
    def EvalCKKStoFHEW(self, ciphertext: Ciphertext, numCtxts: int = 0) -> list[LWECiphertext]:
        ...
    def EvalCKKStoFHEWKeyGen(self, keyPair: KeyPair, lwesk: LWEPrivateKey, dim1: int = 0, L: int = 1) -> None:
        ...
    def EvalCKKStoFHEWPrecompute(self, scale: float = 1.0) -> None:
        ...
    def EvalCKKStoFHEWSetup(self, sl: SecurityLevel = ..., slBin: BINFHE_PARAMSET = ..., arbFunc: bool = False, logQ: int = 25, dynamic: bool = False, numSlotsCKKS: int = 0, logQswitch: int = 27) -> tuple[BinFHEContext, LWEPrivateKey]:
        ...
    def EvalChebyshevFunction(self, func: typing.Callable[[float], float], ciphertext: Ciphertext, a: float, b: float, degree: int) -> Ciphertext:
        """
            Method for calculating Chebyshev evaluation on a ciphertext for a smooth input function over the range [a,b]. Supported only in CKKS.
        
            :param func: the function to be approximated
            :type func: function
            :param ciphertext: input ciphertext
            :type ciphertext: Ciphertext
            :param a: lower bound of argument for which the coefficients were found
            :type a: float
            :param b: upper bound of argument for which the coefficients were found
            :type b: float
            :param degree: Desired degree of approximation
            :type degree: int
            :return: the coefficients of the Chebyshev approximation.
            :rtype: Ciphertext
        """
    def EvalChebyshevSeries(self, ciphertext: Ciphertext, coefficients: list[float], a: float, b: float) -> Ciphertext:
        """
            Method for evaluating Chebyshev polynomial interpolation; first the range [a,b] is mapped to [-1,1] using linear transformation 1 + 2 (x-a)/(b-a) If the degree of the polynomial is less than 5, use EvalChebyshevSeriesLinear (naive linear method), otherwise, use EvalChebyshevSeriesPS (Paterson-Stockmeyer method). Supported only in CKKS.
        
            :param ciphertext: input ciphertext
            :type ciphertext: Ciphertext
            :param coefficients: is the vector of coefficients in Chebyshev expansion
            :type coefficients: list
            :param a: lower bound of argument for which the coefficients were found
            :type a: float
            :param b: upper bound of argument for which the coefficients were found
            :type b: float
            :return: the result of polynomial evaluation
            :rtype: Ciphertext
        """
    def EvalChebyshevSeriesLinear(self, ciphertext: Ciphertext, coefficients: list[float], a: float, b: float) -> Ciphertext:
        """
            Naive linear method for evaluating Chebyshev polynomial interpolation; first the range [a,b] is mapped to [-1,1] using linear transformation 1 + 2 (x-a)/(b-a). Supported only in CKKS.
        
            :param ciphertext: input ciphertext
            :type ciphertext: Ciphertext
            :param coefficients:  is the vector of coefficients in Chebyshev expansion
            :type coefficients: list
            :param a: lower bound of argument for which the coefficients were found
            :type a: float
            :param b: upper bound of argument for which the coefficients were found
            :type b: float
            :return: the result of polynomial evaluation
            :rtype: Ciphertext
        """
    def EvalChebyshevSeriesPS(self, ciphertext: Ciphertext, coefficients: list[float], a: float, b: float) -> Ciphertext:
        """
            Paterson-Stockmeyer method for evaluating Chebyshev polynomial interpolation; first the range [a,b] is mapped to [-1,1] using linear transformation 1 + 2 (x-a)/(b-a). Supported only in CKKS.
        
            :param ciphertext: input ciphertext
            :type ciphertext: Ciphertext
            :param coefficients: is the vector of coefficients in Chebyshev expansion
            :type coefficients: list
            :param a: lower bound of argument for which the coefficients were found
            :type a: float
            :param b: upper bound of argument for which the coefficients were found
            :type b: float
            :return: the result of polynomial evaluation
            :rtype: Ciphertext
        """
    def EvalCompareSchemeSwitching(self, ciphertext1: Ciphertext, ciphertext2: Ciphertext, numCtxts: int = 0, numSlots: int = 0, pLWE: int = 0, scaleSign: float = 1.0, unit: bool = False) -> Ciphertext:
        ...
    def EvalCompareSwitchPrecompute(self, pLWE: int = 0, initLevel: int = 0, scaleSign: float = 1.0, unit: bool = False) -> None:
        ...
    def EvalCos(self, ciphertext: Ciphertext, a: float, b: float, degree: int) -> Ciphertext:
        """
            Evaluate approximate cosine function on a ciphertext using the Chebyshev approximation. Supported only in CKKS.
        
            :param ciphertext: input ciphertext
            :type ciphertext: Ciphertext
            :param a: lower bound of argument for which the coefficients were found
            :type a: float
            :param b: upper bound of argument for which the coefficients were found
            :type b: float
            :param degree: Desired degree of approximation
            :type degree: int
            :return: the result of polynomial evaluation.
            :rtype: Ciphertext
        """
    def EvalDivide(self, ciphertext: Ciphertext, a: float, b: float, degree: int) -> Ciphertext:
        """
            Evaluate approximate division function 1/x where x >= 1 on a ciphertext using the Chebyshev approximation. Supported only in CKKS.
        
            :param ciphertext: input ciphertext
            :type ciphertext: Ciphertext
            :param a: lower bound of argument for which the coefficients were found
            :type a: float
            :param b: upper bound of argument for which the coefficients were found
            :type b: float
            :param degree: Desired degree of approximation
            :type degree: int
            :return: the result of polynomial evaluation.
            :rtype: Ciphertext
        """
    def EvalFHEWtoCKKS(self, LWECiphertexts: list[LWECiphertext], numCtxts: int = 0, numSlots: int = 0, p: int = 4, pmin: float = 0.0, pmax: float = 2.0) -> Ciphertext:
        ...
    def EvalFHEWtoCKKSKeyGen(self, keyPair: KeyPair, lwesk: LWEPrivateKey, numSlots: int = 0, dim1: int = 0, L: int = 0) -> None:
        ...
    def EvalFHEWtoCKKSSetup(self, ccLWE: BinFHEContext, numSlotsCKKS: int = 0, logQ: int = 25) -> None:
        ...
    def EvalFastRotation(self, ciphertext: Ciphertext, index: int, m: int, digits: Ciphertext) -> Ciphertext:
        """
            EvalFastRotation implements the automorphism and key switching step of hoisted automorphisms.
        
            Please refer to Section 5 of Halevi and Shoup, "Faster Homomorphic
            linear transformations in HELib." for more details, link:
            https://eprint.iacr.org/2018/244.
        
            Generally, automorphisms are performed with three steps:
            (1) The automorphism is applied to the ciphertext.
            (2) The automorphed values are decomposed into digits.
            (3) Key switching is applied to enable further computations on the ciphertext.
        
            Hoisted automorphisms are a technique that performs the digit decomposition for the original ciphertext first,
            and then performs the automorphism and the key switching on the decomposed digits.
            The benefit of this is that the digit decomposition is independent of the automorphism rotation index,
            so it can be reused for multiple different indices.
            This can greatly improve performance when we have to compute many automorphisms on the same ciphertext.
            This routinely happens when we do permutations (EvalPermute).
        
            EvalFastRotation implements the automorphism and key switching step of hoisted automorphisms.
        
            This method assumes that all required rotation keys exist.
            This may not be true if we are using baby-step/giant-step key switching.
            Please refer to Section 5.1 of the above reference and EvalPermuteBGStepHoisted to see how to deal with this issue.
        
            :param ciphertext:  the input ciphertext to perform the automorphism on
            :type ciphertext: Ciphertext
            :param index: the index of the rotation. Positive indices correspond to left rotations and negative indices correspond to right rotations.
            :type index: int
            :param m: is the cyclotomic order
            :type m: int
            :param digits: the precomputed ciphertext created by EvalFastRotationPrecompute using the digit decomposition at the precomputation step
            :type digits: Ciphertext
            :return: the rotated ciphertext
            :rtype: Ciphertext
        """
    def EvalFastRotationExt(self, ciphertext: Ciphertext, index: int, digits: Ciphertext, addFirst: bool) -> Ciphertext:
        """
            Only supported for hybrid key switching. Performs fast (hoisted) rotation and returns the results in the extended CRT basis P*Q
        
            :param ciphertext: input ciphertext
            :type ciphertext: Ciphertext
            :param index: the rotation index
            :type index: int
            :param digits: the precomputed ciphertext created by EvalFastRotationPrecompute
            :type digits: Ciphertext
            :param addFirst: if true, the first element c0 is also computed (otherwise ignored)
            :type addFirst: bool
            :return: resulting ciphertext
            :rtype: Ciphertext
        """
    def EvalFastRotationPrecompute(self, ciphertext: Ciphertext) -> Ciphertext:
        """
            EvalFastRotationPrecompute implements the precomputation step of hoisted automorphisms.
        
            Please refer to Section 5 of Halevi and Shoup, "Faster Homomorphic
            linear transformations in HELib." for more details, link:
            https://eprint.iacr.org/2018/244.
        
            Generally, automorphisms are performed with three steps:
            (1) The automorphism is applied to the ciphertext.
            (2) The automorphed values are decomposed into digits.
            (3) Key switching is applied to enable further computations on the ciphertext.
        
            Hoisted automorphisms are a technique that performs the digit decomposition for the original ciphertext first,
            and then performs the automorphism and the key switching on the decomposed digits.
            The benefit of this is that the digit decomposition is independent of the automorphism rotation index,
            so it can be reused for multiple different indices.
            This can greatly improve performance when we have to compute many automorphisms on the same ciphertext.
            This routinely happens when we do permutations (EvalPermute).
        
            EvalFastRotationPrecompute implements the digit decomposition step of hoisted automorphisms.
        
            :param ciphertext: the input ciphertext on which to do the precomputation (digit decomposition)
            :type ciphertext: Ciphertext
            :return: the precomputed ciphertext created using the digit decomposition
            :rtype: Ciphertext
        """
    @typing.overload
    def EvalInnerProduct(self, ciphertext1: Ciphertext, ciphertext2: Ciphertext, batchSize: int) -> Ciphertext:
        """
            Evaluates inner product in packed encoding (uses EvalSum)
        
            :param ciphertext1: first vector
            :type ciphertext1: Ciphertext
            :param ciphertext2: second vector
            :type ciphertext2: Ciphertext
            :param batchSize: size of the batch to be summed up
            :type batchSize: int
            :return: Ciphertext: resulting ciphertext
            :rtype: Ciphertext
        """
    @typing.overload
    def EvalInnerProduct(self, ciphertext: Ciphertext, plaintext: Plaintext, batchSize: int) -> Ciphertext:
        """
            Evaluates inner product in packed encoding (uses EvalSum)
        
            :param ciphertext: first vector - ciphertext
            :type ciphertext: Ciphertext
            :param plaintext: second vector - plaintext
            :type plaintext: Plaintext
            :param batchSize: size of the batch to be summed up
            :type batchSize: int
            :return: Ciphertext: resulting ciphertext
            :rtype: Ciphertext
        """
    def EvalLogistic(self, ciphertext: Ciphertext, a: float, b: float, degree: int) -> Ciphertext:
        """
            Evaluate approximate logistic function 1/(1 + exp(-x)) on a ciphertext using the Chebyshev approximation. Supported only in CKKS.
        
            :param ciphertext: input ciphertext
            :type ciphertext: Ciphertext
            :param a: lower bound of argument for which the coefficients were found
            :type a: float
            :param b: upper bound of argument for which the coefficients were found
            :type b: float
            :param degree: Desired degree of approximation
            :type degree: int
            :return: the result of polynomial evaluation.
            :rtype: Ciphertext
        """
    def EvalMaxSchemeSwitching(self, ciphertext: Ciphertext, publicKey: PublicKey, numValues: int = 0, numSlots: int = 0, oneHot: bool = True, pLWE: int = 0, scaleSign: float = 1.0) -> list[Ciphertext]:
        ...
    def EvalMaxSchemeSwitchingAlt(self, ciphertext: Ciphertext, publicKey: PublicKey, numValues: int = 0, numSlots: int = 0, oneHot: bool = True, pLWE: int = 0, scaleSign: float = 1.0) -> list[Ciphertext]:
        ...
    def EvalMerge(self, ciphertextVec: list[Ciphertext]) -> Ciphertext:
        """
            Merges multiple ciphertexts with encrypted results in slot 0 into a single ciphertext. The slot assignment is done based on the order of ciphertexts in the vector. Requires the generation of rotation keys for the indices that are needed.
        
            :param ciphertextVec: vector of ciphertexts to be merged.
            :type ciphertextVec: list
            :return: resulting ciphertext
            :rtype: Ciphertext
        """
    def EvalMinSchemeSwitching(self, ciphertext: Ciphertext, publicKey: PublicKey, numValues: int = 0, numSlots: int = 0, oneHot: bool = True, pLWE: int = 0, scaleSign: float = 1.0) -> list[Ciphertext]:
        ...
    def EvalMinSchemeSwitchingAlt(self, ciphertext: Ciphertext, publicKey: PublicKey, numValues: int = 0, numSlots: int = 0, oneHot: bool = True, pLWE: int = 0, scaleSign: float = 1.0) -> list[Ciphertext]:
        ...
    @typing.overload
    def EvalMult(self, ciphertext1: Ciphertext, ciphertext2: Ciphertext) -> Ciphertext:
        """
        EvalMult - OpenFHE EvalMult method for a pair of ciphertexts (uses a relinearization key from the crypto context)
        
        :param ciphertext1: multiplier
        :type ciphertext1: Ciphertext
        :param ciphertext2: multiplicand
        :type ciphertext2: Ciphertext
        :return: new ciphertext for ciphertext1 * ciphertext2
        :rtype: Ciphertext
        """
    @typing.overload
    def EvalMult(self, ciphertext: Ciphertext, constant: float) -> Ciphertext:
        """
        Multiplication of a ciphertext by a real number. Supported only in CKKS.
        
        :param ciphertext: multiplier
        :type ciphertext: Ciphertext
        :param constant: multiplicand
        :type constant: float
        :return: the result of multiplication
        :rtype: Ciphertext
        """
    @typing.overload
    def EvalMult(self, ciphertext: Ciphertext, plaintext: Plaintext) -> Ciphertext:
        """
        Multiplication of a ciphertext by a plaintext
        
        :param ciphertext: multiplier
        :type ciphertext: Ciphertext
        :param plaintext: multiplicand
        :type plaintext: Plaintext
        :return: the result of multiplication
        :rtype: Ciphertext
        """
    @typing.overload
    def EvalMult(self, plaintext: Plaintext, ciphertext: Ciphertext) -> Ciphertext:
        ...
    @typing.overload
    def EvalMult(self, constant: float, ciphertext: Ciphertext) -> Ciphertext:
        ...
    def EvalMultAndRelinearize(self, ciphertext1: Ciphertext, ciphertext2: Ciphertext) -> Ciphertext:
        """
            Homomorphic multiplication of two ciphertexts followed by relinearization to the lowest level
        
            :param ciphertext1: first input ciphertext
            :type ciphertext1: Ciphertext
            :param ciphertext2: second input ciphertext
            :type ciphertext2: Ciphertext
            :return: new ciphertext
            :rtype: Ciphertext
        """
    def EvalMultKeyGen(self, privateKey: PrivateKey) -> None:
        """
            EvalMultKeyGen creates a key that can be used with the OpenFHE EvalMult operator.
            The new evaluation key is stored in cryptocontext.
        
            :param privateKey: the private key
            :type privateKey: PrivateKey
        """
    def EvalMultKeysGen(self, privateKey: PrivateKey) -> None:
        """
            EvalMultsKeyGen creates a vector evalmult keys that can be used with the OpenFHE EvalMult operator.
            The 1st key (for s^2) is used for multiplication of ciphertexts of depth 1.
            The 2nd key (for s^3) is used for multiplication of ciphertexts of depth 2, etc.
            A vector of new evaluation keys is stored in cryptocontext.
        
            :param privateKey: the private key
            :type privateKey: PrivateKey
        """
    @typing.overload
    def EvalMultMutable(self, ciphertext1: Ciphertext, ciphertext2: Ciphertext) -> Ciphertext:
        """
        EvalMult - OpenFHE EvalMult method for a pair of mutable ciphertexts (uses a relinearization key from the crypto context)
        
        :param ciphertext1: multiplier
        :type ciphertext1: Ciphertext
        :param ciphertext2: multiplicand
        :type ciphertext2: Ciphertext
        :return: new ciphertext for ciphertext1 * ciphertext2
        :rtype: Ciphertext
        """
    @typing.overload
    def EvalMultMutable(self, ciphertext: Ciphertext, plaintext: Plaintext) -> Ciphertext:
        """
        Multiplication of mutable ciphertext and plaintext
        :param ciphertext: multiplier
        :type ciphertext: Ciphertext
        :param plaintext: multiplicand
        :type plaintext: Plaintext
        :return: the result of multiplication
        :rtype: Ciphertext
        """
    @typing.overload
    def EvalMultMutable(self, plaintext: Plaintext, ciphertext: Ciphertext) -> Ciphertext:
        ...
    def EvalMultMutableInPlace(self, ciphertext1: Ciphertext, ciphertext2: Ciphertext) -> None:
        """
            In-place EvalMult method for a pair of mutable ciphertexts (uses a relinearization key from the crypto context)
        
            :param ciphertext1: multiplier
            :type ciphertext1: Ciphertext
            :param ciphertext2: multiplicand
            :type ciphertext2: Ciphertext
        """
    def EvalMultNoRelin(self, ciphertext1: Ciphertext, ciphertext2: Ciphertext) -> Ciphertext:
        """
            Homomorphic multiplication of two ciphertexts without relinearization
        
            :param ciphertext1: multiplier
            :type ciphertext1: Ciphertext
            :param ciphertext2: multiplicand
            :type ciphertext2: Ciphertext
            :return: new ciphertext for ciphertext1 * ciphertext2
            :rtype: Ciphertext
        """
    def EvalNegate(self, ciphertext: Ciphertext) -> Ciphertext:
        """
            Negates a ciphertext
        
            :param ciphertext: input ciphertext
            :type ciphertext: Ciphertext
            :return: new ciphertext: -ciphertext
            :rtype: Ciphertext
        """
    def EvalNegateInPlace(self, ciphertext: Ciphertext) -> None:
        """
            In-place negation of a ciphertext
        
            :param ciphertext: input ciphertext
            :type ciphertext: Ciphertext
        """
    def EvalPoly(self, ciphertext: Ciphertext, coefficients: list[float]) -> Ciphertext:
        """
            Method for polynomial evaluation for polynomials represented as power series.
        
            :param ciphertext: input ciphertext
            :type ciphertext: Ciphertext
            :param coefficients: vector of coefficients in the polynomial; the size of the vector is the degree of the polynomial + 1
            :type coefficients: list
            :return: Ciphertext: the result of polynomial evaluation.
            :rtype: Ciphertext
        """
    def EvalPolyLinear(self, ciphertext: Ciphertext, coefficients: list[float]) -> Ciphertext:
        """
            Naive method for polynomial evaluation for polynomials represented in the power series (fast only for small-degree polynomials; less than 10). Uses a binary tree computation of the polynomial powers. Supported only in CKKS.
        
            :param ciphertext: input ciphertext
            :type ciphertext: Ciphertext
            :param coefficients: is the vector of coefficients in the polynomial; the size of the vector is the degree of the polynomial
            :type coefficients: list
            :return: Ciphertext: the result of polynomial evaluation.
            :rtype: Ciphertext
        """
    def EvalPolyPS(self, ciphertext: Ciphertext, coefficients: list[float]) -> Ciphertext:
        """
            Paterson-Stockmeyer method for evaluation for polynomials represented in the power series. Supported only in CKKS.
        
            :param ciphertext: input ciphertext
            :type ciphertext: Ciphertext
            :param coefficients: is the vector of coefficients in the polynomial; the size of the vector is the degree of the polynomial
            :type coefficients: list
            :return: Ciphertext: the result of polynomial evaluation.
            :rtype: Ciphertext
        """
    def EvalRotate(self, ciphertext: Ciphertext, index: int) -> Ciphertext:
        """
            Rotates a ciphertext by an index (positive index is a left shift, negative index is a right shift). Uses a rotation key stored in a crypto context. Calls EvalAtIndex under the hood.
        
            :param ciphertext: input ciphertext
            :type ciphertext: Ciphertext
            :param index: rotation index
            :type index: int
            :return: a rotated ciphertext
            :rtype: Ciphertext
        """
    def EvalRotateKeyGen(self, privateKey: PrivateKey, indexList: list[int], publicKey: PublicKey = None) -> None:
        """
            EvalRotateKeyGen generates evaluation keys for a list of indices. Calls EvalAtIndexKeyGen under the hood.
        
            :param privateKey: private key
            :type privateKey: PrivateKey
            :param indexList: list of integers representing the indices
            :type indexList: list
            :param publicKey: public key (used in NTRU schemes)
            :type publicKey: PublicKey
        """
    def EvalSchemeSwitchingKeyGen(self, keyPair: KeyPair, lwesk: LWEPrivateKey, numValues: int = 0, oneHot: bool = True, alt: bool = False, dim1CF: int = 0, dim1FC: int = 0, LCF: int = 1, LFC: int = 0) -> None:
        ...
    def EvalSchemeSwitchingSetup(self, sl: SecurityLevel = ..., slBin: BINFHE_PARAMSET = ..., arbFunc: bool = False, logQ: int = 25, dynamic: bool = False, numSlotsCKKS: int = 0, logQswitch: int = 27) -> tuple[BinFHEContext, LWEPrivateKey]:
        ...
    def EvalSin(self, ciphertext: Ciphertext, a: float, b: float, degree: int) -> Ciphertext:
        """
            Evaluate approximate sine function on a ciphertext using the Chebyshev approximation. Supported only in CKKS.
        
            :param ciphertext: input ciphertext
            :type ciphertext: Ciphertext
            :param a: lower bound of argument for which the coefficients were found
            :type a: float
            :param b: upper bound of argument for which the coefficients were found
            :type b: float
            :param degree: Desired degree of approximation
            :type degree: int
            :return: the result of polynomial evaluation.
            :rtype: Ciphertext
        """
    def EvalSquare(self, ciphertext: Ciphertext) -> Ciphertext:
        """
            Efficient homomorphic squaring of a ciphertext - uses a relinearization key stored in the crypto context
        
            :param ciphertext: input ciphertext
            :type ciphertext: Ciphertext
            :return: squared ciphertext
            :rtype: Ciphertext
        """
    def EvalSquareInPlace(self, ciphertext: Ciphertext) -> None:
        """
            In-place homomorphic squaring of a mutable ciphertext - uses a relinearization key stored in the crypto context
        
            :param ciphertext: input ciphertext
            :type ciphertext: Ciphertext
            :return: squared ciphertext
        """
    def EvalSquareMutable(self, ciphertext: Ciphertext) -> Ciphertext:
        """
            Efficient homomorphic squaring of a mutable ciphertext - uses a relinearization key stored in the crypto context
        
            :param ciphertext: input ciphertext
            :type ciphertext: Ciphertext
            :return: squared ciphertext
            :rtype: Ciphertext
        """
    @typing.overload
    def EvalSub(self, ciphertext1: Ciphertext, ciphertext2: Ciphertext) -> Ciphertext:
        """
        Homomorphic subtraction of two ciphertexts
        
        :param ciphertext1: minuend
        :type ciphertext1: Ciphertext
        :param ciphertext2: subtrahend
        :type ciphertext2: Ciphertext
        :return: the result as a new ciphertext
        :rtype: Ciphertext
        """
    @typing.overload
    def EvalSub(self, ciphertext: Ciphertext, constant: float) -> Ciphertext:
        """
        Subtraction of a ciphertext and a real number. Supported only in CKKS.
        
        :param ciphertext: input ciphertext
        :type ciphertext: Ciphertext
        :param constant: a real number
        :type constant: float
        :return: new ciphertext for ciphertext - constant
        :rtype: Ciphertext
        """
    @typing.overload
    def EvalSub(self, constant: float, ciphertext: Ciphertext) -> Ciphertext:
        ...
    @typing.overload
    def EvalSub(self, ciphertext: Ciphertext, plaintext: Plaintext) -> Ciphertext:
        """
        Subtraction of a ciphertext and a real number. Supported only in CKKS.
        
        :param ciphertext: minuend
        :type ciphertext: Ciphertext
        :param plaintext: subtrahend
        :type plaintext: Plaintext
        :return: new ciphertext for ciphertext - plaintext
        :rtype: Ciphertext
        """
    @typing.overload
    def EvalSub(self, plaintext: Plaintext, ciphertext: Ciphertext) -> Ciphertext:
        ...
    @typing.overload
    def EvalSubInPlace(self, ciphertext1: Ciphertext, ciphertext2: Ciphertext) -> None:
        """
        In-place homomorphic subtraction of two ciphertexts
        
        :param ciphertext1: minuend
        :type ciphertext1: Ciphertext
        :param ciphertext2: subtrahend
        :type ciphertext2: Ciphertext
        :return: the result as a new ciphertext
        """
    @typing.overload
    def EvalSubInPlace(self, ciphertext: Ciphertext, constant: float) -> None:
        """
        In-place subtraction of a ciphertext and a real number. Supported only in CKKS.
        
        :param ciphertext: input ciphertext
        :type ciphertext: Ciphertext
        :param constant: a real number
        :type constant: float
        """
    @typing.overload
    def EvalSubInPlace(self, constant: float, ciphertext: Ciphertext) -> None:
        ...
    @typing.overload
    def EvalSubMutable(self, ciphertext1: Ciphertext, ciphertext2: Ciphertext) -> Ciphertext:
        """
        Homomorphic subtraction of two mutable ciphertexts
        
        :param ciphertext1: minuend
        :type ciphertext1: Ciphertext
        :param ciphertext2: subtrahend
        :type ciphertext2: Ciphertext
        :return: the result as a new ciphertext
        """
    @typing.overload
    def EvalSubMutable(self, ciphertext: Ciphertext, plaintext: Plaintext) -> Ciphertext:
        """
        Homomorphic subtraction of mutable ciphertext and plaintext
        
        :param ciphertext: minuend
        :type ciphertext: Ciphertext
        :param plaintext: subtrahend
        :type plaintext: Plaintext
        :return: new ciphertext for ciphertext - plaintext
        """
    @typing.overload
    def EvalSubMutable(self, plaintext: Plaintext, ciphertext: Ciphertext) -> Ciphertext:
        ...
    def EvalSubMutableInPlace(self, ciphertext1: Ciphertext, ciphertext2: Ciphertext) -> None:
        """
            In-place homomorphic subtraction of two mutable ciphertexts
        
            :param ciphertext1: minuend
            :type ciphertext1: Ciphertext
            :param ciphertext2: subtrahend
            :type ciphertext2: Ciphertext
            :return: the updated minuend
        """
    def EvalSum(self, ciphertext: Ciphertext, batchSize: int) -> Ciphertext:
        """
            Function for evaluating a sum of all components in a vector.
        
            :param ciphertext: the input ciphertext
            :type ciphertext: Ciphertext
            :param batchSize: size of the batch
            :type batchSize: int
            :return: resulting ciphertext
            :rtype: Ciphertext
        """
    def EvalSumCols(self, ciphertext: Ciphertext, rowSize: int, evalSumKeyMap: EvalKeyMap) -> Ciphertext:
        """
            Sums all elements over column-vectors in a matrix - works only with packed encoding
        
            :param ciphertext: the input ciphertext
            :type ciphertext: Ciphertext
            :param rowSize: size of rows in the matrix
            :type rowSize: int
            :param evalSumKeyMap: reference to the map of evaluation keys generated by
            :type evalSumKeyMap: EvalKeyMap
            :return: Ciphertext: resulting ciphertext
            :rtype: Ciphertext
        """
    def EvalSumColsKeyGen(self, privateKey: PrivateKey, publicKey: PublicKey = None) -> EvalKeyMap:
        """
            Generates the automorphism keys for EvalSumCols; works only for packed encoding
        
            :param privateKey: private key
            :type privateKey: PrivateKey
            :param publicKey: public key
            :type publicKey: PublicKey
            :return: returns the evaluation keys
            :rtype: EvalKeyMap
        """
    def EvalSumKeyGen(self, privateKey: PrivateKey, publicKey: PublicKey = None) -> None:
        """
            EvalSumKeyGen Generates the key map to be used by EvalSum
        
            :param privateKey: private key
            :type privateKey: PrivateKey
            :param publicKey: public key (used in NTRU schemes)
            :type publicKey: PublicKey
            :return: None
        """
    def EvalSumRows(self, ciphertext: Ciphertext, rowSize: int, evalSumKeyMap: EvalKeyMap, subringDim: int = 0) -> Ciphertext:
        """
            Sums all elements over row-vectors in a matrix - works only with packed encoding
        
            :param ciphertext: the input ciphertext
            :type ciphertext: Ciphertext
            :param rowSize: size of rows in the matrix
            :type rowSize: int
            :param evalSumKeyMap: reference to the map of evaluation keys generated by
            :type evalSumKeyMap: EvalKeyMap
            :param subringDim: the current cyclotomic order/subring dimension. If set to 0, we use the full cyclotomic order.
            :type subringDim: int
            :return: Ciphertext: resulting ciphertext
            :rtype: Ciphertext
        """
    def EvalSumRowsKeyGen(self, privateKey: PrivateKey, publicKey: PublicKey = None, rowSize: int = 0, subringDim: int = 0) -> EvalKeyMap:
        """
            Generate the automorphism keys for EvalSumRows; works only for packed encoding
        
            :param privateKey: private key
            :type privateKey: PrivateKey
            :param publicKey: public key
            :type publicKey: PublicKey
            :param rowSize: size of rows in the matrix
            :type rowSize: int
            :param subringDim: subring dimension (set to cyclotomic order if set to 0)
            :type subringDim: int
            :return: returns the evaluation keys
            :rtype: EvalKeyMap
        """
    def FindAutomorphismIndex(self, idx: int) -> int:
        """
            Finds an automorphism index for a given vector index using a scheme-specific algorithm
        
            :param idx: regular vector index
            :type idx: int
            :return: the automorphism index
            :rtype: int
        """
    def FindAutomorphismIndices(self, idxList: list[int]) -> list[int]:
        """
            Finds automorphism indices for a given list of vector indices using a scheme-specific algorithm
        
            :param idxList: list of indices
            :type idxList: List[int]
            :return: a list of automorphism indices
            :rtype: List[int]
        """
    def GetCyclotomicOrder(self) -> int:
        """
            Get the cyclotomic order used for this context
        
            :return: The cyclotomic order
            :rtype: int
        """
    def GetDigitSize(self) -> int:
        ...
    def GetEvalSumKeyMap(self, arg0: str) -> EvalKeyMap:
        """
            Get a map of summation keys (each is composed of several automorphism keys) for a specific secret key tag
            :return: EvalKeyMap: key map
            :rtype: EvalKeyMap
        """
    def GetKeyGenLevel(self) -> int:
        """
            For future use: getter for the level at which evaluation keys should be generated
        
            :return: The level used for key generation
            :rtype: int
        """
    def GetModulus(self) -> float:
        """
            Get the cyclotomic order used for this context
        
            :return: The modulus
            :rtype: int
        """
    def GetModulusCKKS(self) -> int:
        ...
    def GetPlaintextModulus(self) -> int:
        """
            Get the plaintext modulus used for this context
        
            :return: The plaintext modulus
            :rtype: int
        """
    def GetRingDimension(self) -> int:
        """
            Get the ring dimension used for this context
        
            :return: The ring dimension
            :rtype: int
        """
    def GetScalingFactorReal(self, arg0: int) -> float:
        """
            Method to retrieve the scaling factor of level l. For FIXEDMANUAL scaling technique method always returns 2^p, where p corresponds to plaintext modulus
        
            :param l:  For FLEXIBLEAUTO scaling technique the level whose scaling factor we want to learn. Levels start from 0 (no scaling done - all towers) and go up to K-1, where K is the number of towers supported.
            :type l: int
            :return: the scaling factor.
            :rtype: float
        """
    def GetScalingTechnique(self) -> ScalingTechnique:
        ...
    def IntMPBootAdd(self, sharePairVec: list[list[Ciphertext]]) -> list[Ciphertext]:
        """
            Threshold FHE: Aggregates a vector of masked decryptions and re-encryotion shares, which is the second step of the interactive multiparty bootstrapping procedure.
        
            :param sharesPairVec: vector of pair of ciphertexts, each element of this vector contains (h_0i, h_1i) - the masked-decryption and encryption shares ofparty i
            :type sharesPairVec: List[List[Ciphertext]]
            :return: aggregated pair of shares ((h_0, h_1)
            :rtype: List[Ciphertext]
        """
    def IntMPBootAdjustScale(self, ciphertext: Ciphertext) -> Ciphertext:
        """
            Threshold FHE: Prepare a ciphertext for Multi-Party Interactive Bootstrapping.
        
            :param ciphertext: Input Ciphertext
            :type ciphertext: Ciphertext
            :return: Resulting Ciphertext
            :rtype: Ciphertext
        """
    def IntMPBootDecrypt(self, privateKey: PrivateKey, ciphertext: Ciphertext, a: Ciphertext) -> list[Ciphertext]:
        """
            Threshold FHE: Does masked decryption as part of Multi-Party Interactive Bootstrapping. Each party calls this function as part of the protocol
        
            :param privateKey: secret key share for party i
            :type privateKey: PrivateKey
            :param ciphertext: input ciphertext
            :type ciphertext: Ciphertext
            :param a: input common random polynomial
            :type a: Ciphertext
            :return: Resulting masked decryption
            :rtype: Ciphertext
        """
    def IntMPBootEncrypt(self, publicKey: PublicKey, sharePair: list[Ciphertext], a: Ciphertext, ciphertext: Ciphertext) -> Ciphertext:
        """
            Threshold FHE: Does public key encryption of lead party's masked decryption as part of interactive multi-party bootstrapping, which increases the ciphertext modulus and enables future computations. This operation is done by the lead party as the final step of interactive multi-party bootstrapping.
        
            :param publicKey: the lead party's public key
            :type publicKey: PublicKey
            :param sharesPair: aggregated decryption and re-encryption shares
            :type sharesPair: List[Ciphertext]
            :param a: common random ring element
            :type a: Ciphertext
            :param ciphertext: input ciphertext
            :type ciphertext: Ciphertext
            :return: Resulting encryption
            :rtype: Ciphertext
        """
    def IntMPBootRandomElementGen(self, publicKey: PublicKey) -> Ciphertext:
        """
            Threshold FHE: Generate a common random polynomial for Multi-Party Interactive Bootstrapping
        
            :param publicKey: the scheme public key (you can also provide the lead party's public-key)
            :type publicKey: PublicKey
            :return: Resulting ring element
            :rtype: Ciphertext
        """
    def KeyGen(self) -> KeyPair:
        """
            Generate a public and private key pair
        
            :return: a public/secret key pair
            :rtype: KeyPair
        """
    def KeySwitchGen(self, oldPrivateKey: PrivateKey, newPrivateKey: PrivateKey) -> EvalKey:
        """
            KeySwitchGen creates a key that can be used with the OpenFHE KeySwitch operation
        
            :param oldPrivateKey: input secrey key
            :type oldPrivateKey: PrivateKey
            :param newPrivateKey: output secret key
            :type newPrivateKey: PrivateKey
            :return: new evaluation key
            :rtype: EvalKey
        """
    @typing.overload
    def MakeCKKSPackedPlaintext(self, value: list[complex], scaleDeg: int = 1, level: int = 0, params: ParmType = None, slots: int = 0) -> Plaintext:
        """
            COMPLEX ARITHMETIC IS NOT AVAILABLE, AND THIS METHOD BE DEPRECATED. USE THE REAL-NUMBER METHOD INSTEAD. MakeCKKSPackedPlaintext constructs a CKKSPackedEncoding in this context from a vector of complex numbers
        
            :param value: input vector of complex numbers
            :type value: List[complex]
            :param scaleDeg: degree of scaling factor used to encode the vector
            :type scaleDeg: int
            :param level: level at each the vector will get encrypted
            :type level: int
            :param params: parameters to be used for the ciphertext (Only accepting params = None in this version)
            :type params: openfhe.ParmType
            :param slots: number of slots
            :type slots: int
            :return: plaintext
            :rtype: Plaintext
        """
    @typing.overload
    def MakeCKKSPackedPlaintext(self, value: list[float], scaleDeg: int = 1, level: int = 0, params: ParmType = None, slots: int = 0) -> Plaintext:
        """
            MakeCKKSPlaintext constructs a CKKSPackedEncoding in this context from a vector of real numbers
        
            :param value: input vector (of floats)
            :type value: list
            :param scaleDeg: degree of scaling factor used to encode the vector
            :type scaleDeg: int
            :param level: level at each the vector will get encrypted
            :type level: int
            :param params: parameters to be used for the ciphertext (Only accepting params = None in this version)
            :type params: openfhe.ParmType
            :param slots: number of slots
            :type slots: int
            :return: plaintext
            :rtype: Plaintext
        """
    def MakeCoefPackedPlaintext(self, value: list[int], noiseScaleDeg: int = 1, level: int = 0) -> Plaintext:
        """
            MakeCoefPackedPlaintext constructs a CoefPackedEncoding in this context
        
            :param value: vector of signed integers mod t
            :type value: List[int]
            :param noiseScaleDeg :  is degree of the scaling factor to encode the plaintext at
            :type noiseScaleDeg : int
            :param level: is the level to encode the plaintext at
            :type level: int
            :return: plaintext
            :rtype: Plaintext
        """
    def MakePackedPlaintext(self, value: list[int], noiseScaleDeg: int = 1, level: int = 0) -> Plaintext:
        """
            MakePackedPlaintext constructs a PackedEncoding in this context
        
            :param value: vector of signed integers mod t
            :type value: List[int]
            :param noiseScaleDeg: is degree of the scaling factor to encode the plaintext at
            :type noiseScaleDeg: int
            :param level: is the level to encode the plaintext at
            :type level: int
            :return: plaintext
            :rtype: Plaintext
        """
    def MakeStringPlaintext(self, str: str) -> Plaintext:
        """
            MakeStringPlaintext constructs a StringEncoding in this context.
        
            :param str: string to be encoded
            :type str: str
            :return: plaintext
        """
    def ModReduce(self, ciphertext: Ciphertext) -> Ciphertext:
        """
            ModReduce - OpenFHE ModReduce method used only for BGV/CKKS.
        
            :param ciphertext: ciphertext
            :type ciphertext: Ciphertext
            :return: Ciphertext: mod reduced ciphertext
            :rtype: Ciphertext
        """
    def ModReduceInPlace(self, ciphertext: Ciphertext) -> None:
        """
            ModReduce - OpenFHE ModReduceInPlace method used only for BGV/CKKS.
        
            :param ciphertext: ciphertext to be mod-reduced in-place
            :type ciphertext: Ciphertext
        """
    def MultiAddEvalKeys(self, evalKey1: EvalKey, evalKey2: EvalKey, keyId: str = '') -> EvalKey:
        """
            Threshold FHE: Adds two prior evaluation keys
        
            :param evalKey1: first evaluation key
            :type evalKey1: EvalKey
            :param evalKey2: second evaluation key
            :type evalKey2: EvalKey
            :param keyId: new key identifier used for resulting evaluation key
            :type keyId: str
            :return: the new joined key
            :rtype: EvalKey
        """
    def MultiAddEvalMultKeys(self, evalKey1: EvalKey, evalKey2: EvalKey, keyId: str = '') -> EvalKey:
        """
            Threshold FHE: Adds two prior evaluation key sets for summation
        
            :param evalKey1: first evaluation key
            :type evalKey1: EvalKey
            :param evalKey2: second evaluation key
            :type evalKey2: EvalKey
            :param keyId: new key identifier used for resulting evaluation key
            :type keyId: str
            :return: the new joined key
            :rtype: EvalKey
        """
    def MultiAddEvalSumKeys(self, evalKeyMap1: EvalKeyMap, evalKeyMap2: EvalKeyMap, keyId: str = '') -> EvalKeyMap:
        """
            Threshold FHE: Adds two prior evaluation key sets for summation
        
            :param evalKeyMap1: first summation key set
            :type evalKeyMap1: EvalKeyMap
            :param evalKeyMap2: second summation key set
            :type evalKeyMap2: EvalKeyMap
            :param keyId: new key identifier used for resulting evaluation key
            :type keyId: str
            :return: the neew joined key set for summation
            :rtype: EvalKeyMap
        """
    def MultiEvalSumKeyGen(self, privateKey: PrivateKey, evalKeyMap: EvalKeyMap, keyId: str = '') -> EvalKeyMap:
        """
            Threshold FHE: Generates joined summation evaluation keys from the current secret share and prior joined summation keys
        
            :param privateKey: secret key share
            :type privateKey: PrivateKey
            :param evalKeyMap: a map with prior joined summation keys
            :type evalKeyMap: EvalKeyMap
            :param keyId: new key identifier used for resulting evaluation key
            :type keyId: str
            :return: EvalKeyMap: new joined summation keys
            :rtype: EvalKeyMap
        """
    def MultiKeySwitchGen(self, originalPrivateKey: PrivateKey, newPrivateKey: PrivateKey, evalKey: EvalKey) -> EvalKey:
        """
            Threshold FHE: Generates a joined evaluation key from the current secret share and a prior joined evaluation key
        
            :param originalPrivateKey: secret key transformed from.
            :type originalPrivateKey: PrivateKey
            :param newPrivateKey: secret key transformed from.
            :type newPrivateKey: PrivateKey
            :param evalKey: the prior joined evaluation key.
            :type evalKey: EvalKey
            :return: EvalKey: the new joined evaluation key.
            :rtype: EvalKey
        """
    def MultiMultEvalKey(self, privateKey: PrivateKey, evalKey: EvalKey, keyId: str = '') -> EvalKey:
        """
            Threshold FHE: Generates a partial evaluation key for homomorphic multiplication based on the current secret share and an existing partial evaluation key
        
            :param privateKey: current secret share
            :type privateKey: PrivateKey
            :param evalKey: prior evaluation key
            :type evalKey: EvalKey
            :param keyId: new key identifier used for resulting evaluation key
            :type keyId: str
            :return: the new joined key
            :rtype: EvalKey
        """
    def MultipartyDecryptFusion(self, ciphertextVec: list[Ciphertext]) -> Plaintext:
        """
            Threshold FHE: Method for combining the partially decrypted ciphertexts and getting the final decryption in the clear.
        
            :param partialCiphertextVec: list of "partial" decryptions
            :type partialCiphertextVec: list
            :return: Plaintext: resulting plaintext
            :rtype: Plaintext
        """
    def MultipartyDecryptLead(self, ciphertextVec: list[Ciphertext], privateKey: PrivateKey) -> list[Ciphertext]:
        """
            Threshold FHE: Method for decryption operation run by the lead decryption client
        
            :param ciphertextVec: a list of ciphertexts
            :type ciphertextVec: list
            :param privateKey:  secret key share used for decryption.
            :type privateKey: PrivateKey
            :return: list of partially decrypted ciphertexts.
            :rtype: List[Ciphertext]
        """
    def MultipartyDecryptMain(self, ciphertextVec: list[Ciphertext], privateKey: PrivateKey) -> list[Ciphertext]:
        """
            Threshold FHE: "Partial" decryption computed by all parties except for the lead one
        
            :param ciphertextVec: a list of ciphertexts
            :type ciphertextVec: list
            :param privateKey:  secret key share used for decryption.
            :type privateKey: PrivateKey
            :return: list of partially decrypted ciphertexts.
            :rtype: List[Ciphertext]
        """
    @typing.overload
    def MultipartyKeyGen(self, publicKey: PublicKey, makeSparse: bool = False, fresh: bool = False) -> KeyPair:
        """
            Threshold FHE: Generation of a public key derived from a previous joined public key (for prior secret shares) and the secret key share of the current party.
        
            :param publicKey:  joined public key from prior parties.
            :type publicKey: PublicKey
            :param makeSparse: set to true if ring reduce by a factor of 2 is to be used. NOT SUPPORTED BY ANY SCHEME ANYMORE.
            :type makeSparse: bool
            :param fresh: set to true if proxy re-encryption is used in the multi-party protocol or star topology is used
            :type fresh: bool
            :return: KeyPair: key pair including the secret share for the current party and joined public key
            :rtype: KeyPair
        """
    @typing.overload
    def MultipartyKeyGen(self, privateKeyVec: list[PrivateKey]) -> KeyPair:
        """
            Threshold FHE: Generates a public key from a vector of secret shares. ONLY FOR DEBUGGIN PURPOSES. SHOULD NOT BE USED IN PRODUCTION.
        
            :param privateKeyVec: secret key shares.
            :type privateKeyVec: List[PrivateKey]
            :return KeyPair: key pair including the private for the current party and joined public key
            :rtype: KeyPair
        """
    def ReEncrypt(self, ciphertext: Ciphertext, evalKey: EvalKey, publicKey: PublicKey = None) -> Ciphertext:
        """
            ReEncrypt - Proxy Re-Encryption mechanism for OpenFHE
        
            :param ciphertext: input ciphertext
            :type ciphertext: Ciphertext
            :param evalKey: evaluation key for PRE keygen method
            :type evalKey: EvalKey
            :param publicKey: the public key of the recipient of the reencrypted ciphertext
            :type publicKey: PublicKey
            :return: the resulting ciphertext
            :rtype: Ciphertext
        """
    def ReKeyGen(self, oldPrivateKey: PrivateKey, newPublicKey: PublicKey) -> EvalKey:
        """
            ReKeyGen produces an Eval Key that OpenFHE can use for Proxy Re-Encryption
        
            :param oldPrivateKey: original private key
            :type privateKey: PrivateKey
            :param newPublicKey: public key
            :type publicKey: PublicKey
            :return: new evaluation key
            :rtype: EvalKey
        """
    def Relinearize(self, ciphertext: Ciphertext) -> Ciphertext:
        """
            Homomorphic multiplication of two ciphertexts withour relinearization
        
            :param ciphertext: input ciphertext
            :type ciphertext: Ciphertext
            :return: relinearized ciphertext
            :rtype: Ciphertext
        """
    def RelinearizeInPlace(self, ciphertext: Ciphertext) -> None:
        """
            In-place relinearization of a ciphertext to the lowest level (with 2 polynomials per ciphertext).
        
            :param ciphertext: input ciphertext
            :type ciphertext: Ciphertext
        """
    def Rescale(self, ciphertext: Ciphertext) -> Ciphertext:
        """
            Rescale - An alias for OpenFHE ModReduce method. This is because ModReduce is called Rescale in CKKS.
        
            :param ciphertext: ciphertext
            :type ciphertext: Ciphertext
            :return: Ciphertext: rescaled ciphertext
            :rtype: Ciphertext
        """
    def RescaleInPlace(self, ciphertext: Ciphertext) -> None:
        """
            Rescale - An alias for OpenFHE ModReduceInPlace method. This is because ModReduceInPlace is called RescaleInPlace in CKKS.
        
            :param ciphertext:  ciphertext to be rescaled in-place
            :type ciphertext: Ciphertext
        """
    def SetKeyGenLevel(self, level: int) -> None:
        """
            For future use: setter for the level at which evaluation keys should be generated
        
            :param level: the level to set the key generation to
            :type level: int
        """
    def __init__(self) -> None:
        ...
    def get_ptr(self) -> None:
        ...
class DecryptionNoiseMode:
    """
    Members:
    
      FIXED_NOISE_DECRYPT
    
      NOISE_FLOODING_DECRYPT
    """
    FIXED_NOISE_DECRYPT: typing.ClassVar[DecryptionNoiseMode]  # value = <DecryptionNoiseMode.FIXED_NOISE_DECRYPT: 0>
    NOISE_FLOODING_DECRYPT: typing.ClassVar[DecryptionNoiseMode]  # value = <DecryptionNoiseMode.NOISE_FLOODING_DECRYPT: 1>
    __members__: typing.ClassVar[dict[str, DecryptionNoiseMode]]  # value = {'FIXED_NOISE_DECRYPT': <DecryptionNoiseMode.FIXED_NOISE_DECRYPT: 0>, 'NOISE_FLOODING_DECRYPT': <DecryptionNoiseMode.NOISE_FLOODING_DECRYPT: 1>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class EncryptionTechnique:
    """
    Members:
    
      STANDARD
    
      EXTENDED
    """
    EXTENDED: typing.ClassVar[EncryptionTechnique]  # value = <EncryptionTechnique.EXTENDED: 1>
    STANDARD: typing.ClassVar[EncryptionTechnique]  # value = <EncryptionTechnique.STANDARD: 0>
    __members__: typing.ClassVar[dict[str, EncryptionTechnique]]  # value = {'STANDARD': <EncryptionTechnique.STANDARD: 0>, 'EXTENDED': <EncryptionTechnique.EXTENDED: 1>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class EvalKey:
    def GetKeyTag(self) -> str:
        ...
    def SetKeyTag(self, arg0: str) -> None:
        ...
    def __init__(self) -> None:
        ...
class EvalKeyMap:
    def __init__(self) -> None:
        ...
class ExecutionMode:
    """
    Members:
    
      EXEC_EVALUATION
    
      EXEC_NOISE_ESTIMATION
    """
    EXEC_EVALUATION: typing.ClassVar[ExecutionMode]  # value = <ExecutionMode.EXEC_EVALUATION: 0>
    EXEC_NOISE_ESTIMATION: typing.ClassVar[ExecutionMode]  # value = <ExecutionMode.EXEC_NOISE_ESTIMATION: 1>
    __members__: typing.ClassVar[dict[str, ExecutionMode]]  # value = {'EXEC_EVALUATION': <ExecutionMode.EXEC_EVALUATION: 0>, 'EXEC_NOISE_ESTIMATION': <ExecutionMode.EXEC_NOISE_ESTIMATION: 1>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class FHECKKSRNS:
    @staticmethod
    @typing.overload
    def GetBootstrapDepth(arg0: int, arg1: list[int], arg2: SecretKeyDist) -> int:
        ...
    @staticmethod
    @typing.overload
    def GetBootstrapDepth(arg0: list[int], arg1: SecretKeyDist) -> int:
        ...
    def __init__(self) -> None:
        ...
class Format:
    """
    Members:
    
      EVALUATION
    
      COEFFICIENT
    """
    COEFFICIENT: typing.ClassVar[Format]  # value = <Format.COEFFICIENT: 1>
    EVALUATION: typing.ClassVar[Format]  # value = <Format.EVALUATION: 0>
    __members__: typing.ClassVar[dict[str, Format]]  # value = {'EVALUATION': <Format.EVALUATION: 0>, 'COEFFICIENT': <Format.COEFFICIENT: 1>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class KEYGEN_MODE:
    """
    Members:
    
      SYM_ENCRYPT
    
      PUB_ENCRYPT
    """
    PUB_ENCRYPT: typing.ClassVar[KEYGEN_MODE]  # value = <KEYGEN_MODE.PUB_ENCRYPT: 1>
    SYM_ENCRYPT: typing.ClassVar[KEYGEN_MODE]  # value = <KEYGEN_MODE.SYM_ENCRYPT: 0>
    __members__: typing.ClassVar[dict[str, KEYGEN_MODE]]  # value = {'SYM_ENCRYPT': <KEYGEN_MODE.SYM_ENCRYPT: 0>, 'PUB_ENCRYPT': <KEYGEN_MODE.PUB_ENCRYPT: 1>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class KeyPair:
    publicKey: PublicKey
    secretKey: PrivateKey
    def good(self) -> bool:
        """
            Checks whether both public key and secret key are non-null, or correctly initialized.
        
            :return: Result.
            :rtype: bool
        """
class KeySwitchTechnique:
    """
    Members:
    
      INVALID_KS_TECH
    
      BV
    
      HYBRID
    """
    BV: typing.ClassVar[KeySwitchTechnique]  # value = <KeySwitchTechnique.BV: 1>
    HYBRID: typing.ClassVar[KeySwitchTechnique]  # value = <KeySwitchTechnique.HYBRID: 2>
    INVALID_KS_TECH: typing.ClassVar[KeySwitchTechnique]  # value = <KeySwitchTechnique.INVALID_KS_TECH: 0>
    __members__: typing.ClassVar[dict[str, KeySwitchTechnique]]  # value = {'INVALID_KS_TECH': <KeySwitchTechnique.INVALID_KS_TECH: 0>, 'BV': <KeySwitchTechnique.BV: 1>, 'HYBRID': <KeySwitchTechnique.HYBRID: 2>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class LWECiphertext:
    __hash__: typing.ClassVar[None] = None
    def GetLength(self) -> int:
        ...
    def GetModulus(self) -> int:
        ...
    def __eq__(self, arg0: LWECiphertext) -> bool:
        ...
    def __init__(self) -> None:
        ...
    def __ne__(self, arg0: LWECiphertext) -> bool:
        ...
class LWEPrivateKey:
    __hash__: typing.ClassVar[None] = None
    def GetLength(self) -> int:
        ...
    def __eq__(self, arg0: LWEPrivateKey) -> bool:
        ...
    def __init__(self) -> None:
        ...
    def __ne__(self, arg0: LWEPrivateKey) -> bool:
        ...
class MultipartyMode:
    """
    Members:
    
      INVALID_MULTIPARTY_MODE
    
      FIXED_NOISE_MULTIPARTY
    
      NOISE_FLOODING_MULTIPARTY
    """
    FIXED_NOISE_MULTIPARTY: typing.ClassVar[MultipartyMode]  # value = <MultipartyMode.FIXED_NOISE_MULTIPARTY: 1>
    INVALID_MULTIPARTY_MODE: typing.ClassVar[MultipartyMode]  # value = <MultipartyMode.INVALID_MULTIPARTY_MODE: 0>
    NOISE_FLOODING_MULTIPARTY: typing.ClassVar[MultipartyMode]  # value = <MultipartyMode.NOISE_FLOODING_MULTIPARTY: 2>
    __members__: typing.ClassVar[dict[str, MultipartyMode]]  # value = {'INVALID_MULTIPARTY_MODE': <MultipartyMode.INVALID_MULTIPARTY_MODE: 0>, 'FIXED_NOISE_MULTIPARTY': <MultipartyMode.FIXED_NOISE_MULTIPARTY: 1>, 'NOISE_FLOODING_MULTIPARTY': <MultipartyMode.NOISE_FLOODING_MULTIPARTY: 2>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class MultiplicationTechnique:
    """
    Members:
    
      BEHZ
    
      HPS
    
      HPSPOVERQ
    
      HPSPOVERQLEVELED
    """
    BEHZ: typing.ClassVar[MultiplicationTechnique]  # value = <MultiplicationTechnique.BEHZ: 0>
    HPS: typing.ClassVar[MultiplicationTechnique]  # value = <MultiplicationTechnique.HPS: 1>
    HPSPOVERQ: typing.ClassVar[MultiplicationTechnique]  # value = <MultiplicationTechnique.HPSPOVERQ: 2>
    HPSPOVERQLEVELED: typing.ClassVar[MultiplicationTechnique]  # value = <MultiplicationTechnique.HPSPOVERQLEVELED: 3>
    __members__: typing.ClassVar[dict[str, MultiplicationTechnique]]  # value = {'BEHZ': <MultiplicationTechnique.BEHZ: 0>, 'HPS': <MultiplicationTechnique.HPS: 1>, 'HPSPOVERQ': <MultiplicationTechnique.HPSPOVERQ: 2>, 'HPSPOVERQLEVELED': <MultiplicationTechnique.HPSPOVERQLEVELED: 3>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class PKESchemeFeature:
    """
    Members:
    
      PKE
    
      KEYSWITCH
    
      PRE
    
      LEVELEDSHE
    
      ADVANCEDSHE
    
      MULTIPARTY
    
      FHE
    
      SCHEMESWITCH
    """
    ADVANCEDSHE: typing.ClassVar[PKESchemeFeature]  # value = <PKESchemeFeature.ADVANCEDSHE: 16>
    FHE: typing.ClassVar[PKESchemeFeature]  # value = <PKESchemeFeature.FHE: 64>
    KEYSWITCH: typing.ClassVar[PKESchemeFeature]  # value = <PKESchemeFeature.KEYSWITCH: 2>
    LEVELEDSHE: typing.ClassVar[PKESchemeFeature]  # value = <PKESchemeFeature.LEVELEDSHE: 8>
    MULTIPARTY: typing.ClassVar[PKESchemeFeature]  # value = <PKESchemeFeature.MULTIPARTY: 32>
    PKE: typing.ClassVar[PKESchemeFeature]  # value = <PKESchemeFeature.PKE: 1>
    PRE: typing.ClassVar[PKESchemeFeature]  # value = <PKESchemeFeature.PRE: 4>
    SCHEMESWITCH: typing.ClassVar[PKESchemeFeature]  # value = <PKESchemeFeature.SCHEMESWITCH: 128>
    __members__: typing.ClassVar[dict[str, PKESchemeFeature]]  # value = {'PKE': <PKESchemeFeature.PKE: 1>, 'KEYSWITCH': <PKESchemeFeature.KEYSWITCH: 2>, 'PRE': <PKESchemeFeature.PRE: 4>, 'LEVELEDSHE': <PKESchemeFeature.LEVELEDSHE: 8>, 'ADVANCEDSHE': <PKESchemeFeature.ADVANCEDSHE: 16>, 'MULTIPARTY': <PKESchemeFeature.MULTIPARTY: 32>, 'FHE': <PKESchemeFeature.FHE: 64>, 'SCHEMESWITCH': <PKESchemeFeature.SCHEMESWITCH: 128>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class ParmType:
    pass
class Plaintext:
    def Decode(self) -> bool:
        """
            Decode the polynomial into a plaintext.
        """
    def Encode(self) -> bool:
        """
            Encode the plaintext into a polynomial.
        """
    def GetCKKSPackedValue(self) -> list[complex]:
        """
            Get the packed value of the plaintext for CKKS-based plaintexts.
        
            :return: The packed value of the plaintext.
            :rtype: List[complex]
        """
    def GetLength(self) -> int:
        """
            Get method to return the length of the plaintext.
        
            :return: The length of the plaintext in terms of the number of bits.
            :rtype: int
        """
    def GetLevel(self) -> int:
        ...
    def GetLogError(self) -> float:
        ...
    @typing.overload
    def GetLogPrecision(self) -> float:
        """
            Get the log of the plaintext precision.
        
            :return: The log of the plaintext precision.
            :rtype: float
        """
    @typing.overload
    def GetLogPrecision(self) -> float:
        ...
    def GetNoiseScaleDeg(self) -> int:
        ...
    def GetPackedValue(self) -> list[int]:
        ...
    def GetRealPackedValue(self) -> list[float]:
        """
            Get the real component of the packed value of the plaintext for CKKS-based plaintexts.
        
            :return: The real-component of the packed value of the plaintext.
            :rtype: List[double]
        """
    def GetScalingFactor(self) -> float:
        """
            Get the scaling factor of the plaintext for CKKS-based plaintexts.
        
            :return: The scaling factor of the plaintext.
            :rtype: float
        """
    @typing.overload
    def GetSchemeID(self) -> SCHEME:
        """
            Get the encryption technique of the plaintext for BFV-based plaintexts.
        
            :return: The scheme ID of the plaintext.
            :rtype: SCHEME
        """
    @typing.overload
    def GetSchemeID(self) -> SCHEME:
        """
            Get the encryption technique of the plaintext for BFV-based plaintexts.
        
            :return: The scheme ID of the plaintext.
            :rtype: SCHEME
        """
    def GetSlots(self) -> int:
        ...
    def GetStringValue(self) -> str:
        ...
    def HighBound(self) -> int:
        """
            Calculate and return upper bound that can be encoded with the plaintext modulus the number to encode MUST be less than this value
        
            :return: floor(p/2)
            :rtype: int
        """
    def IsEncoded(self) -> bool:
        """
            Check if the plaintext is encoded.
        
            :return: True if the plaintext is encoded, False otherwise.
            :rtype: bool
        """
    def LowBound(self) -> int:
        """
            Calculate and return lower bound that can be encoded with the plaintext modulus the number to encode MUST be greater than this value
        
            :return: floor(-p/2)
            :rtype: int
        """
    def SetFormat(self, fmt: Format) -> None:
        """
            SetFormat - allows format to be changed for openfhe.Plaintext evaluations
        
            :param fmt:
            :type format: Format
        """
    def SetIntVectorValue(self, arg0: list[int]) -> None:
        ...
    def SetLength(self, newSize: int) -> None:
        """
            Resize the plaintext; only works for plaintexts that support a resizable vector (coefpacked).
            
            :param newSize: The new size of the plaintext.
            :type newSize: int
        """
    def SetLevel(self, arg0: int) -> None:
        ...
    def SetNoiseScaleDeg(self, arg0: int) -> None:
        ...
    def SetScalingFactor(self, sf: float) -> None:
        """
            Set the scaling factor of the plaintext for CKKS-based plaintexts.
        
            :param sf: The scaling factor to set.
            :type sf: float
        """
    def SetSlots(self, arg0: int) -> None:
        ...
    def SetStringValue(self, arg0: str) -> None:
        ...
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
class PrivateKey:
    def GetKeyTag(self) -> str:
        ...
    def SetKeyTag(self, arg0: str) -> None:
        ...
    def __init__(self) -> None:
        ...
class ProxyReEncryptionMode:
    """
    Members:
    
      NOT_SET
    
      INDCPA
    
      FIXED_NOISE_HRA
    
      NOISE_FLOODING_HRA
    
      DIVIDE_AND_ROUND_HRA
    """
    DIVIDE_AND_ROUND_HRA: typing.ClassVar[ProxyReEncryptionMode]  # value = <ProxyReEncryptionMode.DIVIDE_AND_ROUND_HRA: 4>
    FIXED_NOISE_HRA: typing.ClassVar[ProxyReEncryptionMode]  # value = <ProxyReEncryptionMode.FIXED_NOISE_HRA: 2>
    INDCPA: typing.ClassVar[ProxyReEncryptionMode]  # value = <ProxyReEncryptionMode.INDCPA: 1>
    NOISE_FLOODING_HRA: typing.ClassVar[ProxyReEncryptionMode]  # value = <ProxyReEncryptionMode.NOISE_FLOODING_HRA: 3>
    NOT_SET: typing.ClassVar[ProxyReEncryptionMode]  # value = <ProxyReEncryptionMode.NOT_SET: 0>
    __members__: typing.ClassVar[dict[str, ProxyReEncryptionMode]]  # value = {'NOT_SET': <ProxyReEncryptionMode.NOT_SET: 0>, 'INDCPA': <ProxyReEncryptionMode.INDCPA: 1>, 'FIXED_NOISE_HRA': <ProxyReEncryptionMode.FIXED_NOISE_HRA: 2>, 'NOISE_FLOODING_HRA': <ProxyReEncryptionMode.NOISE_FLOODING_HRA: 3>, 'DIVIDE_AND_ROUND_HRA': <ProxyReEncryptionMode.DIVIDE_AND_ROUND_HRA: 4>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class PublicKey:
    def GetKeyTag(self) -> str:
        ...
    def SetKeyTag(self, arg0: str) -> None:
        ...
    def __init__(self) -> None:
        ...
class SCHEME:
    """
    Members:
    
      INVALID_SCHEME
    
      CKKSRNS_SCHEME
    
      BFVRNS_SCHEME
    
      BGVRNS_SCHEME
    """
    BFVRNS_SCHEME: typing.ClassVar[SCHEME]  # value = <SCHEME.BFVRNS_SCHEME: 2>
    BGVRNS_SCHEME: typing.ClassVar[SCHEME]  # value = <SCHEME.BGVRNS_SCHEME: 3>
    CKKSRNS_SCHEME: typing.ClassVar[SCHEME]  # value = <SCHEME.CKKSRNS_SCHEME: 1>
    INVALID_SCHEME: typing.ClassVar[SCHEME]  # value = <SCHEME.INVALID_SCHEME: 0>
    __members__: typing.ClassVar[dict[str, SCHEME]]  # value = {'INVALID_SCHEME': <SCHEME.INVALID_SCHEME: 0>, 'CKKSRNS_SCHEME': <SCHEME.CKKSRNS_SCHEME: 1>, 'BFVRNS_SCHEME': <SCHEME.BFVRNS_SCHEME: 2>, 'BGVRNS_SCHEME': <SCHEME.BGVRNS_SCHEME: 3>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class SERBINARY:
    pass
class SERJSON:
    pass
class ScalingTechnique:
    """
    Members:
    
      FIXEDMANUAL
    
      FIXEDAUTO
    
      FLEXIBLEAUTO
    
      FLEXIBLEAUTOEXT
    
      NORESCALE
    
      INVALID_RS_TECHNIQUE
    """
    FIXEDAUTO: typing.ClassVar[ScalingTechnique]  # value = <ScalingTechnique.FIXEDAUTO: 1>
    FIXEDMANUAL: typing.ClassVar[ScalingTechnique]  # value = <ScalingTechnique.FIXEDMANUAL: 0>
    FLEXIBLEAUTO: typing.ClassVar[ScalingTechnique]  # value = <ScalingTechnique.FLEXIBLEAUTO: 2>
    FLEXIBLEAUTOEXT: typing.ClassVar[ScalingTechnique]  # value = <ScalingTechnique.FLEXIBLEAUTOEXT: 3>
    INVALID_RS_TECHNIQUE: typing.ClassVar[ScalingTechnique]  # value = <ScalingTechnique.INVALID_RS_TECHNIQUE: 5>
    NORESCALE: typing.ClassVar[ScalingTechnique]  # value = <ScalingTechnique.NORESCALE: 4>
    __members__: typing.ClassVar[dict[str, ScalingTechnique]]  # value = {'FIXEDMANUAL': <ScalingTechnique.FIXEDMANUAL: 0>, 'FIXEDAUTO': <ScalingTechnique.FIXEDAUTO: 1>, 'FLEXIBLEAUTO': <ScalingTechnique.FLEXIBLEAUTO: 2>, 'FLEXIBLEAUTOEXT': <ScalingTechnique.FLEXIBLEAUTOEXT: 3>, 'NORESCALE': <ScalingTechnique.NORESCALE: 4>, 'INVALID_RS_TECHNIQUE': <ScalingTechnique.INVALID_RS_TECHNIQUE: 5>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class SecretKeyDist:
    """
    Members:
    
      GAUSSIAN
    
      UNIFORM_TERNARY
    
      SPARSE_TERNARY
    """
    GAUSSIAN: typing.ClassVar[SecretKeyDist]  # value = <SecretKeyDist.GAUSSIAN: 0>
    SPARSE_TERNARY: typing.ClassVar[SecretKeyDist]  # value = <SecretKeyDist.SPARSE_TERNARY: 2>
    UNIFORM_TERNARY: typing.ClassVar[SecretKeyDist]  # value = <SecretKeyDist.UNIFORM_TERNARY: 1>
    __members__: typing.ClassVar[dict[str, SecretKeyDist]]  # value = {'GAUSSIAN': <SecretKeyDist.GAUSSIAN: 0>, 'UNIFORM_TERNARY': <SecretKeyDist.UNIFORM_TERNARY: 1>, 'SPARSE_TERNARY': <SecretKeyDist.SPARSE_TERNARY: 2>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class SecurityLevel:
    """
    Members:
    
      HEStd_128_classic
    
      HEStd_192_classic
    
      HEStd_256_classic
    
      HEStd_NotSet
    """
    HEStd_128_classic: typing.ClassVar[SecurityLevel]  # value = <SecurityLevel.HEStd_128_classic: 0>
    HEStd_192_classic: typing.ClassVar[SecurityLevel]  # value = <SecurityLevel.HEStd_192_classic: 1>
    HEStd_256_classic: typing.ClassVar[SecurityLevel]  # value = <SecurityLevel.HEStd_256_classic: 2>
    HEStd_NotSet: typing.ClassVar[SecurityLevel]  # value = <SecurityLevel.HEStd_NotSet: 6>
    __members__: typing.ClassVar[dict[str, SecurityLevel]]  # value = {'HEStd_128_classic': <SecurityLevel.HEStd_128_classic: 0>, 'HEStd_192_classic': <SecurityLevel.HEStd_192_classic: 1>, 'HEStd_256_classic': <SecurityLevel.HEStd_256_classic: 2>, 'HEStd_NotSet': <SecurityLevel.HEStd_NotSet: 6>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
@typing.overload
def DeserializeCiphertext(filename: str, sertype: SERJSON) -> tuple[Ciphertext, bool]:
    ...
@typing.overload
def DeserializeCiphertext(filename: str, sertype: SERBINARY) -> tuple[Ciphertext, bool]:
    ...
@typing.overload
def DeserializeCryptoContext(filename: str, sertype: SERJSON) -> tuple[CryptoContext, bool]:
    ...
@typing.overload
def DeserializeCryptoContext(filename: str, sertype: SERBINARY) -> tuple[CryptoContext, bool]:
    ...
@typing.overload
def DeserializeEvalKey(filename: str, sertype: SERJSON) -> tuple[EvalKey, bool]:
    ...
@typing.overload
def DeserializeEvalKey(filename: str, sertype: SERBINARY) -> tuple[EvalKey, bool]:
    ...
@typing.overload
def DeserializePrivateKey(filename: str, sertype: SERJSON) -> tuple[PrivateKey, bool]:
    ...
@typing.overload
def DeserializePrivateKey(filename: str, sertype: SERBINARY) -> tuple[PrivateKey, bool]:
    ...
@typing.overload
def DeserializePublicKey(filename: str, sertype: SERJSON) -> tuple[PublicKey, bool]:
    ...
@typing.overload
def DeserializePublicKey(filename: str, sertype: SERBINARY) -> tuple[PublicKey, bool]:
    ...
@typing.overload
def GenCryptoContext(params: CCParamsBFVRNS) -> CryptoContext:
    ...
@typing.overload
def GenCryptoContext(params: CCParamsBGVRNS) -> CryptoContext:
    ...
@typing.overload
def GenCryptoContext(params: CCParamsCKKSRNS) -> CryptoContext:
    ...
def GetAllContexts() -> list[CryptoContext]:
    ...
def ReleaseAllContexts() -> None:
    ...
@typing.overload
def SerializeToFile(filename: str, obj: CryptoContext, sertype: SERJSON) -> bool:
    ...
@typing.overload
def SerializeToFile(filename: str, obj: PublicKey, sertype: SERJSON) -> bool:
    ...
@typing.overload
def SerializeToFile(filename: str, obj: PrivateKey, sertype: SERJSON) -> bool:
    ...
@typing.overload
def SerializeToFile(filename: str, obj: Ciphertext, sertype: SERJSON) -> bool:
    ...
@typing.overload
def SerializeToFile(filename: str, obj: EvalKey, sertype: SERJSON) -> bool:
    ...
@typing.overload
def SerializeToFile(filename: str, obj: CryptoContext, sertype: SERBINARY) -> bool:
    ...
@typing.overload
def SerializeToFile(filename: str, obj: PublicKey, sertype: SERBINARY) -> bool:
    ...
@typing.overload
def SerializeToFile(filename: str, obj: PrivateKey, sertype: SERBINARY) -> bool:
    ...
@typing.overload
def SerializeToFile(filename: str, obj: Ciphertext, sertype: SERBINARY) -> bool:
    ...
@typing.overload
def SerializeToFile(filename: str, obj: EvalKey, sertype: SERBINARY) -> bool:
    ...
def get_native_int() -> int:
    ...
ADVANCEDSHE: PKESchemeFeature  # value = <PKESchemeFeature.ADVANCEDSHE: 16>
AND: BINGATE  # value = <BINGATE.AND: 1>
AP: BINFHE_METHOD  # value = <BINFHE_METHOD.AP: 1>
BEHZ: MultiplicationTechnique  # value = <MultiplicationTechnique.BEHZ: 0>
BFVRNS_SCHEME: SCHEME  # value = <SCHEME.BFVRNS_SCHEME: 2>
BGVRNS_SCHEME: SCHEME  # value = <SCHEME.BGVRNS_SCHEME: 3>
BINARY: SERBINARY  # value = <openfhe.openfhe.SERBINARY object>
BOOTSTRAPPED: BINFHE_OUTPUT  # value = <BINFHE_OUTPUT.BOOTSTRAPPED: 2>
BV: KeySwitchTechnique  # value = <KeySwitchTechnique.BV: 1>
CKKSRNS_SCHEME: SCHEME  # value = <SCHEME.CKKSRNS_SCHEME: 1>
COEFFICIENT: Format  # value = <Format.COEFFICIENT: 1>
COMPACT: COMPRESSION_LEVEL  # value = <COMPRESSION_LEVEL.COMPACT: 2>
DIVIDE_AND_ROUND_HRA: ProxyReEncryptionMode  # value = <ProxyReEncryptionMode.DIVIDE_AND_ROUND_HRA: 4>
EVALUATION: Format  # value = <Format.EVALUATION: 0>
EXEC_EVALUATION: ExecutionMode  # value = <ExecutionMode.EXEC_EVALUATION: 0>
EXEC_NOISE_ESTIMATION: ExecutionMode  # value = <ExecutionMode.EXEC_NOISE_ESTIMATION: 1>
EXTENDED: EncryptionTechnique  # value = <EncryptionTechnique.EXTENDED: 1>
FHE: PKESchemeFeature  # value = <PKESchemeFeature.FHE: 64>
FIXEDAUTO: ScalingTechnique  # value = <ScalingTechnique.FIXEDAUTO: 1>
FIXEDMANUAL: ScalingTechnique  # value = <ScalingTechnique.FIXEDMANUAL: 0>
FIXED_NOISE_DECRYPT: DecryptionNoiseMode  # value = <DecryptionNoiseMode.FIXED_NOISE_DECRYPT: 0>
FIXED_NOISE_HRA: ProxyReEncryptionMode  # value = <ProxyReEncryptionMode.FIXED_NOISE_HRA: 2>
FIXED_NOISE_MULTIPARTY: MultipartyMode  # value = <MultipartyMode.FIXED_NOISE_MULTIPARTY: 1>
FLEXIBLEAUTO: ScalingTechnique  # value = <ScalingTechnique.FLEXIBLEAUTO: 2>
FLEXIBLEAUTOEXT: ScalingTechnique  # value = <ScalingTechnique.FLEXIBLEAUTOEXT: 3>
FRESH: BINFHE_OUTPUT  # value = <BINFHE_OUTPUT.FRESH: 1>
GAUSSIAN: SecretKeyDist  # value = <SecretKeyDist.GAUSSIAN: 0>
GINX: BINFHE_METHOD  # value = <BINFHE_METHOD.GINX: 2>
HEStd_128_classic: SecurityLevel  # value = <SecurityLevel.HEStd_128_classic: 0>
HEStd_192_classic: SecurityLevel  # value = <SecurityLevel.HEStd_192_classic: 1>
HEStd_256_classic: SecurityLevel  # value = <SecurityLevel.HEStd_256_classic: 2>
HEStd_NotSet: SecurityLevel  # value = <SecurityLevel.HEStd_NotSet: 6>
HPS: MultiplicationTechnique  # value = <MultiplicationTechnique.HPS: 1>
HPSPOVERQ: MultiplicationTechnique  # value = <MultiplicationTechnique.HPSPOVERQ: 2>
HPSPOVERQLEVELED: MultiplicationTechnique  # value = <MultiplicationTechnique.HPSPOVERQLEVELED: 3>
HYBRID: KeySwitchTechnique  # value = <KeySwitchTechnique.HYBRID: 2>
INDCPA: ProxyReEncryptionMode  # value = <ProxyReEncryptionMode.INDCPA: 1>
INVALID_KS_TECH: KeySwitchTechnique  # value = <KeySwitchTechnique.INVALID_KS_TECH: 0>
INVALID_METHOD: BINFHE_METHOD  # value = <BINFHE_METHOD.INVALID_METHOD: 0>
INVALID_MULTIPARTY_MODE: MultipartyMode  # value = <MultipartyMode.INVALID_MULTIPARTY_MODE: 0>
INVALID_OUTPUT: BINFHE_OUTPUT  # value = <BINFHE_OUTPUT.INVALID_OUTPUT: 0>
INVALID_RS_TECHNIQUE: ScalingTechnique  # value = <ScalingTechnique.INVALID_RS_TECHNIQUE: 5>
INVALID_SCHEME: SCHEME  # value = <SCHEME.INVALID_SCHEME: 0>
JSON: SERJSON  # value = <openfhe.openfhe.SERJSON object>
KEYSWITCH: PKESchemeFeature  # value = <PKESchemeFeature.KEYSWITCH: 2>
LEVELEDSHE: PKESchemeFeature  # value = <PKESchemeFeature.LEVELEDSHE: 8>
LMKCDEY: BINFHE_METHOD  # value = <BINFHE_METHOD.LMKCDEY: 3>
MEDIUM: BINFHE_PARAMSET  # value = <BINFHE_PARAMSET.MEDIUM: 1>
MULTIPARTY: PKESchemeFeature  # value = <PKESchemeFeature.MULTIPARTY: 32>
NAND: BINGATE  # value = <BINGATE.NAND: 3>
NOISE_FLOODING_DECRYPT: DecryptionNoiseMode  # value = <DecryptionNoiseMode.NOISE_FLOODING_DECRYPT: 1>
NOISE_FLOODING_HRA: ProxyReEncryptionMode  # value = <ProxyReEncryptionMode.NOISE_FLOODING_HRA: 3>
NOISE_FLOODING_MULTIPARTY: MultipartyMode  # value = <MultipartyMode.NOISE_FLOODING_MULTIPARTY: 2>
NOR: BINGATE  # value = <BINGATE.NOR: 2>
NORESCALE: ScalingTechnique  # value = <ScalingTechnique.NORESCALE: 4>
NOT_SET: ProxyReEncryptionMode  # value = <ProxyReEncryptionMode.NOT_SET: 0>
OR: BINGATE  # value = <BINGATE.OR: 0>
PKE: PKESchemeFeature  # value = <PKESchemeFeature.PKE: 1>
PRE: PKESchemeFeature  # value = <PKESchemeFeature.PRE: 4>
PUB_ENCRYPT: KEYGEN_MODE  # value = <KEYGEN_MODE.PUB_ENCRYPT: 1>
SCHEMESWITCH: PKESchemeFeature  # value = <PKESchemeFeature.SCHEMESWITCH: 128>
SIGNED_MOD_TEST: BINFHE_PARAMSET  # value = <BINFHE_PARAMSET.SIGNED_MOD_TEST: 23>
SLACK: COMPRESSION_LEVEL  # value = <COMPRESSION_LEVEL.SLACK: 3>
SPARSE_TERNARY: SecretKeyDist  # value = <SecretKeyDist.SPARSE_TERNARY: 2>
STANDARD: EncryptionTechnique  # value = <EncryptionTechnique.STANDARD: 0>
STD128: BINFHE_PARAMSET  # value = <BINFHE_PARAMSET.STD128: 4>
STD128Q: BINFHE_PARAMSET  # value = <BINFHE_PARAMSET.STD128Q: 7>
STD128Q_3: BINFHE_PARAMSET  # value = <BINFHE_PARAMSET.STD128Q_3: 13>
STD128Q_3_LMKCDEY: BINFHE_PARAMSET  # value = <BINFHE_PARAMSET.STD128Q_3_LMKCDEY: 14>
STD128Q_4: BINFHE_PARAMSET  # value = <BINFHE_PARAMSET.STD128Q_4: 19>
STD128Q_4_LMKCDEY: BINFHE_PARAMSET  # value = <BINFHE_PARAMSET.STD128Q_4_LMKCDEY: 20>
STD128Q_LMKCDEY: BINFHE_PARAMSET  # value = <BINFHE_PARAMSET.STD128Q_LMKCDEY: 8>
STD128_3: BINFHE_PARAMSET  # value = <BINFHE_PARAMSET.STD128_3: 11>
STD128_3_LMKCDEY: BINFHE_PARAMSET  # value = <BINFHE_PARAMSET.STD128_3_LMKCDEY: 12>
STD128_4: BINFHE_PARAMSET  # value = <BINFHE_PARAMSET.STD128_4: 17>
STD128_4_LMKCDEY: BINFHE_PARAMSET  # value = <BINFHE_PARAMSET.STD128_4_LMKCDEY: 18>
STD128_AP: BINFHE_PARAMSET  # value = <BINFHE_PARAMSET.STD128_AP: 3>
STD128_LMKCDEY: BINFHE_PARAMSET  # value = <BINFHE_PARAMSET.STD128_LMKCDEY: 2>
STD192: BINFHE_PARAMSET  # value = <BINFHE_PARAMSET.STD192: 5>
STD192Q: BINFHE_PARAMSET  # value = <BINFHE_PARAMSET.STD192Q: 9>
STD192Q_3: BINFHE_PARAMSET  # value = <BINFHE_PARAMSET.STD192Q_3: 15>
STD192Q_4: BINFHE_PARAMSET  # value = <BINFHE_PARAMSET.STD192Q_4: 21>
STD256: BINFHE_PARAMSET  # value = <BINFHE_PARAMSET.STD256: 6>
STD256Q: BINFHE_PARAMSET  # value = <BINFHE_PARAMSET.STD256Q: 10>
STD256Q_3: BINFHE_PARAMSET  # value = <BINFHE_PARAMSET.STD256Q_3: 16>
STD256Q_4: BINFHE_PARAMSET  # value = <BINFHE_PARAMSET.STD256Q_4: 22>
SYM_ENCRYPT: KEYGEN_MODE  # value = <KEYGEN_MODE.SYM_ENCRYPT: 0>
TOY: BINFHE_PARAMSET  # value = <BINFHE_PARAMSET.TOY: 0>
UNIFORM_TERNARY: SecretKeyDist  # value = <SecretKeyDist.UNIFORM_TERNARY: 1>
XNOR: BINGATE  # value = <BINGATE.XNOR: 5>
XNOR_FAST: BINGATE  # value = <BINGATE.XNOR_FAST: 12>
XOR: BINGATE  # value = <BINGATE.XOR: 4>
XOR_FAST: BINGATE  # value = <BINGATE.XOR_FAST: 11>
