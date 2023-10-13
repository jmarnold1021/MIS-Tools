DROP TABLE [dbo].[L56_DOD_SG]
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[L56_DOD_SG]') AND type in (N'U'))
BEGIN
CREATE TABLE [dbo].[L56_DOD_SG](
	[GI01] [varchar](3) NULL,
	[CCCCO_Assigned] [varchar](9) NOT NULL,
	[GI03] [varchar](3) NOT NULL,
	[SG01] [varchar](4) NULL,
	[SG02] [varchar](4) NULL,
	[SG03] [varchar](1) NULL,
	[SG04] [varchar](1) NULL,
	[SG05] [varchar](1) NULL,
	[SG06] [varchar](1) NULL,
	[SG07] [varchar](1) NULL,
	[SG08] [varchar](1) NULL,
	[SG09] [varchar](2) NULL,
	[SG10] [varchar](1) NULL,
	[SG11] [varchar](1) NULL,
	[SG12] [varchar](5) NULL,
	[SG13] [varchar](1) NULL,
	[SG14] [varchar](2) NULL,
	[SG15] [varchar](1) NULL,
	[SG16] [varchar](1) NULL,
	[SG17] [varchar](1) NULL,
	[SG18] [varchar](1) NULL,
	[SG19] [varchar](1) NULL,
	[SG20] [varchar](1) NULL,
	[SG21] [varchar](1) NULL,
	[SG22] [varchar](1) NULL,
	[SG23] [varchar](7) NULL,
	[SG24] [varchar](1) NULL,
	[SG25] [varchar](1) NULL,
	[SG26] [varchar](2) NULL,
 CONSTRAINT [PK_DOD_SG_GI03_CCCCO_Assigned] PRIMARY KEY CLUSTERED 
(
	[GI03] DESC,
	[CCCCO_Assigned] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
END
GO
